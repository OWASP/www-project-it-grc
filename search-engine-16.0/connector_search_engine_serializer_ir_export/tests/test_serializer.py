# Copyright 2023 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo.exceptions import ValidationError
from odoo.tests import Form

from odoo.addons.connector_search_engine.tests.test_all import TestBindingIndexBaseFake


class TestSerializer(TestBindingIndexBaseFake):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._load_fixture(
            "ir_exports_test.xml", "connector_search_engine_serializer_ir_export"
        )
        cls.exporter = cls.env.ref(
            "connector_search_engine_serializer_ir_export.ir_exp_partner_test"
        )
        cls.se_index.write(
            {
                "serializer_type": "ir_exports",
                "exporter_id": cls.exporter.id,
            }
        )

    def test_changing_model_remove_exporter(self):
        index = Form(self.se_index)
        index.model_id = self.env.ref("base.model_res_users")
        self.assertFalse(index.exporter_id)

    def test_serialize(self):
        self.partner_binding.recompute_json()
        self.assertEqual(
            self.partner_binding.data,
            {
                "active": True,
                "child_ids": [
                    {
                        "child_ids": [],
                        "country_id": {"code": "US", "name": "United States"},
                        "email": "docbrown@future.com",
                        "id": self.partner.child_ids.id,
                        "name": "Doc Brown",
                    }
                ],
                "color": 0,
                "country_id": {"code": "US", "name": "United States"},
                "id": self.partner.id,
                "lang": "en_US",
                "name": "Marty McFly",
                "partner_latitude": 0.0,
            },
        )

    def test_exporter_required(self):
        with self.assertRaises(ValidationError):
            self.se_index.exporter_id = None
