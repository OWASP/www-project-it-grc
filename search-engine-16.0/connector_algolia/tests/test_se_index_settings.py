# Copyright 2021 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import mock

from odoo.addons.connector_search_engine.tests.test_all import TestBindingIndexBaseFake

MOCK_PATH = "odoo.addons.connector_search_engine.models.se_index.SeIndex"


class TestAlgoliaBackend(TestBindingIndexBaseFake):
    def test_index_get_settings(self):
        config = self.env["se.index.config"].create({"name": "Facet"})
        config.body = {"attributesForFaceting": ["name"]}
        self.se_index.config_id = config
        # Simulate index model settings merged w/ index config's
        with mock.patch(MOCK_PATH + "._get_settings") as mocked:
            mocked.return_value = {"attributesForFaceting": ["field1", "field2"]}
            settings = self.se_index._get_settings()
            self.assertEqual(
                settings["attributesForFaceting"], ["field1", "field2", "name"]
            )
