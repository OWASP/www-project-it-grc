# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json
from time import sleep

from vcr_unittest import VCRMixin

from odoo.tools import mute_logger

from odoo.addons.connector_search_engine.tests.test_all import TestBindingIndexBase

from ..tools.adapter import ElasticSearchAdapter

# NOTE: if you need to refresh tests, you can fire up an ElasticSearch instance
# using `docker-compose.elasticsearch.example.yml` in this same folder.
# If you are not running in a docker env, you'll need to add an alias
# in /etc/hosts to make "elastic" name point to 127.0.0.1


class TestConnectorElasticsearch(VCRMixin, TestBindingIndexBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend = cls.env.ref("connector_elasticsearch.backend_1")
        cls.setup_records()
        cls.adapter: ElasticSearchAdapter = cls.se_index.se_adapter

    def _get_vcr_kwargs(self, **kwargs):
        return {
            "record_mode": "one",
            "match_on": ["method", "path", "query"],
            "filter_headers": ["Authorization"],
            "decode_compressed_response": True,
        }

    @classmethod
    def setup_records(cls):
        cls.se_config = cls.env["se.index.config"].create(
            {"name": "my_config", "body": {"mappings": {}}}
        )
        return super().setup_records()

    @classmethod
    def _prepare_index_values(cls, backend):
        values = super()._prepare_index_values(backend)
        values.update({"config_id": cls.se_config.id})
        return values

    def test_index_adapter(self):
        # Set partner to be updated with fake vals in data
        self.partner_binding.write({"state": "to_export", "data": {"id": "foo"}})
        # Export index to elasticsearch should be called
        self.se_index.batch_sync()

        # Ensure that call have been done to the cassette
        self.assertTrue(self.cassette.all_played)

        self.assertGreaterEqual(len(self.cassette.requests), 1)
        request = self.cassette.requests[-1]
        self.assertEqual(request.method, "POST")
        self.assertEqual(self.parse_path(request.uri), "/_bulk")
        body = request.body.decode("utf-8")
        lines = [line for line in filter(lambda line: line, body.split("\n"))]
        # we must have 2 lines: 1 for the index op and 1 with data
        self.assertEqual(len(lines), 2)
        index_action = json.loads(lines[0])
        self.assertDictEqual(
            index_action,
            {
                "index": {
                    "_index": "demo_elasticsearch_backend_contact_en_us",
                    "_id": "foo",
                }
            },
        )
        index_data = json.loads(lines[1])
        self.assertDictEqual(index_data, {"id": "foo"})

    def test_index_config_as_str(self):
        self.se_config.write({"body_str": '{"mappings": {"1":1}}'})
        self.assertDictEqual(self.se_config.body, {"mappings": {"1": 1}})
        self.assertEqual(self.se_config.body_str, '{"mappings": {"1":1}}')

    def test_index_adapter_iter(self):
        data = [{"id": "foo"}, {"id": "foo2"}, {"id": "foo3"}]
        self.adapter.clear()
        self.adapter.index(data)
        if self.cassette.dirty:
            # when we record the test we must wait for es
            sleep(2)
        res = [x for x in self.adapter.each()]
        res.sort(key=lambda d: d["id"])
        self.assertListEqual(res, data)

    def test_index_adapter_delete(self):
        data = [{"id": "foo"}, {"id": "foo2"}, {"id": "foo3"}]
        self.adapter.clear()
        self.adapter.index(data)
        if self.cassette.dirty:
            # when we record the test we must wait for es
            sleep(2)
        self.adapter.delete(["foo", "foo3"])
        if self.cassette.dirty:
            # when we record the test we must wait for es
            sleep(2)
        res = [x for x in self.adapter.each()]
        res.sort(key=lambda d: d["id"])
        self.assertListEqual(res, [{"id": "foo2"}])

    @mute_logger("odoo.addons.connector_search_engine.models.se_binding")
    def test_index_adapter_delete_nonexisting_documents(self):
        """We try to delete records that do not exist.
        Because it does not matter, it is just ignored. No exception.
        """
        self.adapter.delete(["donotexist", "donotexisteither"])

    def test_index_adapter_reindex(self):
        data = [{"id": "foo"}, {"id": "foo2"}, {"id": "foo3"}]
        self.adapter.clear()
        self.adapter.index(data)
        index_name = self.adapter._get_current_aliased_index_name()
        next_index_name = self.adapter._get_next_aliased_index_name(index_name)
        if self.cassette.dirty:
            # when we record the test we must wait for es
            sleep(2)
        self.adapter.reindex()
        if self.cassette.dirty:
            # when we record the test we must wait for es
            sleep(2)
        res = [x for x in self.adapter.each()]
        res.sort(key=lambda d: d["id"])
        self.assertListEqual(res, data)
        self.assertEqual(
            self.adapter._get_current_aliased_index_name(), next_index_name
        )
