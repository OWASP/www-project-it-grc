# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
import os
from time import sleep

from vcr_unittest import VCRMixin

from odoo.tools import human_size, mute_logger

from odoo.addons.connector_search_engine.tests.test_all import TestBindingIndexBase

from ..components.adapter import AlgoliaAdapter

# To refresh cassets data:
# 0. prepare your Algolia account
# 1. delete existing cassettes
# 2. set ALGOLIA_APP_ID + ALGOLIA_API_KEY env vars
# 3. WARNING: replace real app id and api key in cassets files when done!


class TestAlgoliaBackend(VCRMixin, TestBindingIndexBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        AlgoliaAdapter._build_component(cls._components_registry)
        cls.backend_specific = cls.env.ref("connector_algolia.se_algolia_demo")
        cls.backend = cls.backend_specific.se_backend_id
        cls.backend_specific.algolia_app_id = os.environ.get(
            "ALGOLIA_APP_ID", "FAKE_APP"
        )
        cls.backend_specific.algolia_api_key = os.environ.get(
            "ALGOLIA_API_KEY", "FAKE_KEY"
        )
        cls.setup_records()
        with cls.backend_specific.work_on("se.index", index=cls.se_index) as work:
            cls.adapter = work.component(usage="se.backend.adapter")

    def _get_vcr_kwargs(self, **kwargs):
        return {
            "record_mode": "once",
            "match_on": ["method", "path", "query"],
            "filter_headers": ["Authorization"],
            "decode_compressed_response": True,
        }

    def test_get_api_credentials(self):
        self.assertEqual(
            self.backend_specific._get_api_credentials(),
            {"password": self.backend_specific.algolia_api_key},
        )

    def test_index_adapter(self):
        data = {"objectID": "IamAnObjectID1", "foo": "bar"}
        self.adapter.index([data])
        self.assertEqual(len(self.cassette.requests), 1)
        request = self.cassette.requests[0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            self.parse_path(request.uri),
            "/1/indexes/demo_algolia_backend_res_partner_binding_fake_en_US" "/batch",
        )
        request_data = json.loads(request.body.decode("utf-8"))["requests"]
        self.assertEqual(len(request_data), 1)
        self.assertEqual(request_data[0]["action"], "updateObject")
        self.assertEqual(request_data[0]["body"], data)

    def test_index_adapter_clear(self):
        self.se_index.clear_index()
        self.assertEqual(len(self.cassette.requests), 1)
        request = self.cassette.requests[0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            self.parse_path(request.uri),
            "/1/indexes/demo_algolia_backend_res_partner_binding_fake_en_US" "/clear",
        )

    def test_index_adapter_clear_settings(self):
        config = self.env["se.index.config"].create(
            {"name": "Facet", "body_str": '{"attributesForFaceting": ["name"]}'}
        )
        self.se_index.config_id = config
        self.se_index.clear_index()
        if self.cassette.dirty:
            # when we record the test we must wait for algolia
            sleep(2)
        # 1 call for clear, 1 call for settings
        self.assertEqual(len(self.cassette.requests), 2)
        request1 = self.cassette.requests[0]
        request2 = self.cassette.requests[1]
        self.assertEqual(request1.method, "POST")
        self.assertEqual(
            self.parse_path(request1.uri),
            "/1/indexes/demo_algolia_backend_res_partner_binding_fake_en_US" "/clear",
        )
        self.assertEqual(request2.method, "PUT")
        self.assertEqual(
            self.parse_path(request2.uri),
            "/1/indexes/demo_algolia_backend_res_partner_binding_fake_en_US"
            "/settings",
        )
        # use another cassette to isolate this query
        # which is needed only to verify the result.
        # If you don't isolate it, you find 3 requests in the main cassette
        # which is not what you expect when running normally.
        cassette = "TestAlgoliaBackend." "test_index_adapter_clear_settings_GET.yaml"
        kwargs = self._get_vcr_kwargs()
        myvcr = self._get_vcr(**kwargs)
        with myvcr.use_cassette(cassette):
            adapter = self.se_index._get_backend_adapter()
            algolia_index = adapter.get_index()
            settings = algolia_index.get_settings()
            self.assertEqual(settings["attributesForFaceting"], ["name"])

    def test_delete_adapter(self):
        self.adapter.delete(["IamAnObjectID"])
        self.assertEqual(len(self.cassette.requests), 1)
        request = self.cassette.requests[0]
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            self.parse_path(request.uri),
            "/1/indexes/demo_algolia_backend_res_partner_binding_fake_en_US" "/batch",
        )
        request_data = json.loads(request.body.decode("utf-8"))["requests"]
        self.assertEqual(len(request_data), 1)
        self.assertEqual(request_data[0]["action"], "deleteObject")
        self.assertEqual(request_data[0]["body"], {"objectID": "IamAnObjectID"})

    def test_iter_adapter(self):
        data = [{"objectID": "foo"}]
        self.adapter.clear()
        self.adapter.index(data)
        if self.cassette.dirty:
            # when we record the test we must wait for algolia
            sleep(2)
        res = [x for x in self.adapter.each()]
        self.assertEqual(res, data)

    @mute_logger("odoo.addons.connector_search_engine.models.se_binding")
    def test_missing_object_key(self):
        self.record_id_export_line.unlink()
        res = self.partner_binding.recompute_json()
        error_string = "\n".join(
            ["Validation errors", "{}: The key `objectID` is missing in:"]
        ).format(str(self.partner_binding))
        self.assertTrue(res.startswith(error_string))

    def test_added_object_key(self):
        self.assertTrue(self.partner_binding.data)
        self.assertIn("objectID", self.partner_binding.data)
        self.assertEqual(
            self.partner_binding.data["objectID"], self.partner_binding.record_id.id
        )

    def test_customize_object_key(self):
        self.env["ir.exports.line"].create(
            {"export_id": self.exporter.id, "name": "id:objectID"}
        )
        self.partner_binding.recompute_json()
        self.assertTrue(self.partner_binding.data)
        self.assertIn("objectID", self.partner_binding.data)
        self.assertEqual(self.partner_binding.data["objectID"], self.partner_binding.id)

    def test_index_size(self):
        self.assertTrue(self.partner_binding.data)
        self.assertEqual(
            self.partner_binding.data_size,
            human_size(self.partner_binding._get_bytes_size()),
        )
        self.partner_binding.data = {}
        self.assertEqual(self.partner_binding.data_size, "2.00 bytes")
