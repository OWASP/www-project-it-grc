# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import time
from typing import Any, Iterator

from odoo import _
from odoo.exceptions import UserError

from odoo.addons.connector_search_engine.tools.adapter import SearchEngineAdapter

_logger = logging.getLogger(__name__)


try:
    import elasticsearch
    import elasticsearch.helpers
except ImportError:
    _logger.debug("Can not import elasticsearch")


def _is_delete_nonexistent_documents(elastic_exception):
    """True iff all errors in this exception are deleting a nonexisting document."""
    b = lambda d: "delete" in d and d["delete"]["status"] == 404  # noqa
    return all(b(error) for error in elastic_exception.errors)


class ElasticSearchAdapter(SearchEngineAdapter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__es_client = None

    @property
    def _index_name(self):
        return self.index_record.name.lower()

    @property
    def _es_connection_class(self):
        return elasticsearch.RequestsHttpConnection

    @property
    def _es_client(self):
        if not self.__es_client:
            self.__es_client = self._get_es_client()
        return self.__es_client

    @property
    def _index_config(self):
        return self.index_record.config_id.body

    def _get_es_client(self):
        backend = self.backend_record
        api_key = (
            (backend.api_key_id, backend.api_key)
            if backend.api_key_id and backend.api_key
            else None
        )
        return elasticsearch.Elasticsearch(
            [backend.es_server_host],
            connection_class=self._es_connection_class,
            api_key=api_key,
        )

    def test_connection(self):
        es = self._es_client
        try:
            es.security.authenticate()
        except elasticsearch.NotFoundError as exc:
            raise UserError(_("Unable to reach host.")) from exc
        except elasticsearch.AuthenticationException as exc:
            raise UserError(_("Unable to authenticate. Check credentials.")) from exc
        except Exception as exc:
            raise UserError(_("Unable to connect :") + "\n\n" + repr(exc)) from exc

    def index(self, records) -> None:
        es = self._es_client
        records_for_bulk = [
            {
                "_index": self._index_name,
                "_id": record["id"],
                "_source": record,
            }
            for record in records
        ]
        res = elasticsearch.helpers.bulk(es, records_for_bulk)
        # checks if number of indexed object and object in records are equal
        if not res[0] == len(records):
            raise SystemError(
                _(
                    "Unable to index all records. (indexed: %(indexed)s, "
                    "total: %(total)s)\n%(result)s",
                    indexed=res[0],
                    total=len(records),
                    result=res,
                )
            )

    def delete(self, binding_ids) -> None:
        es = self._es_client
        records_for_bulk = []
        for binding_id in binding_ids:
            action = {
                "_op_type": "delete",
                "_index": self._index_name,
                "_id": binding_id,
            }
            records_for_bulk.append(action)
        try:
            elasticsearch.helpers.bulk(es, records_for_bulk)
        except elasticsearch.helpers.errors.BulkIndexError as e:
            # if the document we are trying to delete does not exist,
            # we can consider deletion a success (there is nothing to do).
            if not _is_delete_nonexistent_documents(e):
                raise e
            msg = "Trying to delete non-existent documents. Ignored: %s"
            _logger.info(msg, e)

    def clear(self) -> None:
        es = self._es_client
        index_name = self._get_current_aliased_index_name() or self._index_name
        res = es.indices.delete(index=index_name, ignore=[400, 404])
        self.settings()
        if not res["acknowledged"]:
            raise SystemError(
                _(
                    "Unable to clear index %(index_name)s: %(result)",
                    index_name=index_name,
                    result=res,
                )
            )

    def each(self) -> Iterator[dict[str, Any]]:
        es = self._es_client
        res = es.search(index=self._index_name, filter_path=["hits.hits._source"])
        if not res:
            # eg: empty index
            return
        hits = res["hits"]["hits"]
        for hit in hits:
            yield hit["_source"]

    def settings(self) -> None:
        es = self._es_client
        if not es.indices.exists(self._index_name):
            client = self._es_client
            # To allow rolling updates, we work with index aliases
            aliased_index_name = self._get_next_aliased_index_name()
            client.indices.create(index=aliased_index_name, body=self._index_config)
            client.indices.put_alias(index=aliased_index_name, name=self._index_name)
            msg = "Missing index %s created."
            _logger.info(msg, self._index_name)
        # TODO: understand how to handle this only for dynamic indexes.
        # For non dynamic indexes you should delete the index and reindex.
        # if not created and force:
        #     es.indices.put_settings(self.work.index.config_id.body, index=index_name)

    def _get_current_aliased_index_name(self) -> str:
        """Get the current aliased index name if any"""
        current_aliased_index_name = None
        alias = self._es_client.indices.get_alias(
            name=self._index_name, ignore=[400, 404]
        )
        if "error" not in alias:
            current_aliased_index_name = next(iter(alias))  # get the first key
        return current_aliased_index_name

    def _get_next_aliased_index_name(
        self, aliased_index_name: str | None = None
    ) -> str:
        """Get the next aliased index name

        The next aliased index name is based on the current aliased index name.
        It's the current aliased index name incremented by 1.

        :param aliased_index_name: the current aliased index name
        :return: the next aliased index name
        """
        next_version = 1
        if aliased_index_name:
            next_version = int(aliased_index_name.split("-")[-1]) + 1
        return "%s-%d" % (self._index_name, next_version)

    def reindex(self) -> None:
        """Reindex records according to the current config
        This method is useful to allows a rolling update of index
        configuration.
        This process is based on the following steps:
        1. create a new index with the current config
        2. trigger a reindex into SE from the current index to the new one
        3. Update the index alias to point to the new index
        4. Drop the old index.
        """
        client = self._es_client
        current_aliased_index_name = self._get_current_aliased_index_name()
        next_aliased_index_name = self._get_next_aliased_index_name(
            current_aliased_index_name
        )
        # create new idx
        client.indices.create(index=next_aliased_index_name, body=self._index_config)
        task_def = client.reindex(
            {
                "source": {"index": self._index_name},
                "dest": {"index": next_aliased_index_name},
            },
            request_timeout=9999999,
            wait_for_completion=False,
        )
        while True:
            time.sleep(5)
            _logger.info("Waiting for task completion %s", task_def)
            task = client.tasks.get(task_id=task_def["task"], wait_for_completion=False)
            if task.get("completed"):
                break
        if current_aliased_index_name:
            client.indices.update_aliases(
                body={
                    "actions": [
                        {
                            "remove": {
                                "index": current_aliased_index_name,
                                "alias": self._index_name,
                            },
                        },
                        {
                            "add": {
                                "index": next_aliased_index_name,
                                "alias": self._index_name,
                            }
                        },
                    ]
                }
            )
            client.indices.delete(index=current_aliased_index_name, ignore=[400, 404])
        else:
            # This code will only be triggered the first time the reindex is
            # called on an index created before the use of index aliases.
            client.indices.delete(index=self._index_name, ignore=[400, 404])
            client.indices.put_alias(
                index=next_aliased_index_name, name=self._index_name
            )
