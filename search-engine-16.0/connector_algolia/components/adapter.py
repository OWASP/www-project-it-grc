# Copyright 2016 Akretion (http://www.akretion.com)
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


import logging

from odoo import exceptions

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


try:
    from algoliasearch.search_client import SearchClient
except ImportError:  # pragma: no cover
    _logger.debug("Can not import algoliasearch")


class AlgoliaAdapter(Component):
    _name = "algolia.adapter"
    _inherit = ["se.backend.adapter", "algolia.se.connector"]
    _usage = "se.backend.adapter"

    def get_index(self):
        client = self._get_client()
        return self._get_index(client)

    def _get_client(self):
        backend = self.backend_record
        account = backend._get_api_credentials()
        return SearchClient.create(backend.algolia_app_id, account["password"])

    def _get_index(self, client):
        return client.init_index(self.work.index.name)

    def settings(self, force=False):
        """Push advanced settings like facettings attributes."""
        client = self._get_client()
        index = self._get_index(client)
        data = self.work.index._get_settings()
        if not force:
            # export settings if it is the first creation of the index.
            indexes = client.list_indexes()
            index_names = [item.get("name") for item in indexes.get("items", [])]
            force = index.index_name not in index_names or False
        if data and force:
            index.set_settings(data)

    def index(self, records):
        index = self.get_index()
        for record in records:
            error = self._validate_record(record)
            if error:
                raise exceptions.ValidationError(error)
        index.save_objects(records)

    def delete(self, binding_ids):
        index = self.get_index()
        index.delete_objects(binding_ids)

    def clear(self):
        index = self.get_index()
        index.clear_objects()
        self.settings(force=True)

    def iter(self):
        # `iter` is a built-in keyword -> to be replaced
        _logger.warning("DEPRECATED: use `each` instead of `iter`.")
        return self.each()

    def each(self):
        index = self.get_index()
        return index.browse_objects()
