# Copyright 2018 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import mock

from odoo_test_helper import FakeModelLoader

from odoo.tests.common import Form
from odoo.tools import mute_logger

from odoo.addons.queue_job.job import identity_exact
from odoo.addons.queue_job.tests.common import trap_jobs

from .common import TestSeBackendCaseBase


class TestBindingIndexBase(TestSeBackendCaseBase, FakeModelLoader):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load fake models ->/
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .models import (
            FakeSeAdapter,
            FakeSerializer,
            ResPartner,
            SeBackend,
            SeIndex,
        )

        cls.loader.update_registry((ResPartner, SeBackend, SeIndex))
        cls.binding_model = cls.env["se.binding"]
        cls.se_index_model = cls.env["se.index"]

        cls.se_adapter = FakeSeAdapter
        cls.model_serializer = FakeSerializer

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    @classmethod
    def _prepare_index_values(cls, backend=None):
        backend = backend or cls.backend
        return {
            "name": "Partner Index",
            "backend_id": backend.id,
            "model_id": cls.env["ir.model"]
            .search([("model", "=", "res.partner")], limit=1)
            .id,
            "lang_id": cls.env.ref("base.lang_en").id,
            "serializer_type": "fake",
        }

    @classmethod
    def setup_records(cls, backend=None):
        backend = backend or cls.backend
        # create an index for partner model
        cls.se_index = cls.se_index_model.create(cls._prepare_index_values(backend))
        # create a binding + partner alltogether
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Marty McFly",
                "country_id": cls.env.ref("base.us").id,
                "email": "marty.mcfly@future.com",
                "child_ids": [
                    (0, 0, {"name": "Doc Brown", "email": "docbrown@future.com"})
                ],
            }
        )
        cls.partner_binding = cls.partner._add_to_index(cls.se_index)

        cls.partner_expected = {"id": cls.partner.id, "name": cls.partner.name}


class TestBindingIndexBaseFake(TestBindingIndexBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.backend_model = cls.env["se.backend"]
        cls.backend = cls.backend_model.create(
            {"name": "Fake SE", "tech_name": "fake_se", "backend_type": "fake"}
        )
        cls.setup_records()


class TestBindingIndex(TestBindingIndexBaseFake):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def assert_index_called(self, calls, action, ids):
        self.assertEqual(
            calls, [{"index": self.se_index, "method": action, "args": ids}]
        )

    # TODO: the following `test_backend*` methods
    # should be splitted to a smaller test case.
    # ATM is not possible since the teardown of this class
    # is going to drop the fake models and make any subsequent test case fail.
    # We should find a way to run tear down at the end of ALL test cases.
    def test_backend_name(self):
        form = Form(self.env["se.backend"])
        form.name = "Á weird nämë plenty of CR@P!"
        # tech name normalized
        self.assertEqual(form.tech_name, "a_weird_name_plenty_of_cr_p")
        self.assertEqual(form.index_prefix_name, "a_weird_name_plenty_of_cr_p")
        form.tech_name = "better_name"
        form.index_prefix_name = "better_prefix"
        form.name = "My search backend"
        # name updated, tech names stay
        self.assertEqual(form.tech_name, "better_name")
        self.assertEqual(form.index_prefix_name, "better_prefix")

    def test_backend_create_tech_defaults(self):
        b1 = self.backend_model.create({"name": "Fake 1", "backend_type": "fake"})
        self.assertEqual(b1.tech_name, "fake_1")
        self.assertEqual(b1.index_prefix_name, "fake_1")
        b2 = self.backend_model.create(
            {"name": "Fake 2", "tech_name": "test2", "backend_type": "fake"}
        )
        self.assertEqual(b2.tech_name, "test2")
        self.assertEqual(b2.index_prefix_name, "test2")
        b3 = self.backend_model.create(
            {
                "name": "Fake 3",
                "tech_name": "test3",
                "index_prefix_name": "baz",
                "backend_type": "fake",
            }
        )
        self.assertEqual(b3.tech_name, "test3")
        self.assertEqual(b3.index_prefix_name, "baz")

    def test_index_name(self):
        self.assertEqual(self.se_index.name, "fake_se_contact_en_US")
        # control indexes' name via prefix tech name
        self.backend.index_prefix_name = "foo_baz"
        # TODO: not sure why this is needed here
        self.se_index.invalidate_recordset()
        self.assertEqual(self.se_index.name, "foo_baz_contact_en_US")
        self.se_index.lang_id = False
        self.se_index.invalidate_recordset()
        self.assertEqual(self.se_index.name, "foo_baz_contact")

    def test_index_custom_name(self):
        self.se_index.custom_tech_name = "something meaningful for me"
        self.assertEqual(
            self.se_index.name, "fake_se_something_meaningful_for_me_en_US"
        )

    def test_model_id_domain(self):
        result = self.se_index._model_id_domain()
        models = result[0][2]
        self.assertIn("res.partner", models)

    def test_index_record(self):
        self.assertEqual(self.partner_binding.state, "to_recompute")
        self.assertFalse(self.partner_binding.date_recomputed)

    def test_unindex_record(self):
        self.partner._remove_from_index(self.se_index)
        self.assertEqual(self.partner_binding.state, "to_delete")

    def test_unlink_record(self):
        self.partner.unlink()
        self.assertEqual(self.partner_binding.state, "to_delete")

    def test_recompute_one_record(self):
        self.partner_binding.recompute_json()
        self.assertEqual(self.partner_binding.state, "to_export")
        self.assertEqual(self.partner_binding.get_export_data(), self.partner_expected)
        self.assertTrue(self.partner_binding.date_recomputed)

    def test_recompute_all_indexes(self):
        self.env["se.index"].recompute_all_index()
        self.assertEqual(self.partner_binding.get_export_data(), self.partner_expected)
        self.assertEqual(self.partner_binding.state, "to_export")
        self.assertTrue(self.partner_binding.date_recomputed)

    def test_force_recompute_all_binding(self):
        with mock.patch.object(type(self.se_index), "recompute_all_binding") as mocked:
            self.se_index.force_recompute_all_binding()
        mocked.assert_called_with(force_export=True)

    def test_force_batch_sync_with_not_exportable_binding(self):
        for state in ("to_recompute", "recomputing", "invalid_data", "recompute_error"):
            self.partner_binding.state = state
            with self.se_adapter.mocked_calls() as calls:
                self.se_index.force_batch_sync()
                self.assertEqual(calls, [])
                self.assertEqual(self.partner_binding.state, state)

    def test_force_batch_sync_with_exportable_binding(self):
        self.partner_binding.recompute_json()
        for state in ("done", "to_export", "exporting"):
            self.partner_binding.state = state
            with self.se_adapter.mocked_calls() as calls:
                self.se_index.force_batch_sync()
                self.assert_index_called(calls, "index", [self.partner_binding.data])
                self.assertEqual(self.partner_binding.state, "done")

    def test_force_batch_sync_with_to_delete_binding(self):
        self.partner_binding.state = "to_delete"
        with self.se_adapter.mocked_calls() as calls:
            self.se_index.force_batch_sync()
            self.assert_index_called(calls, "delete", [self.partner.id])
            self.assertFalse(self.partner_binding.exists())

    def test_force_batch_sync_with_deleting_binding(self):
        self.partner_binding.state = "deleting"
        with self.se_adapter.mocked_calls() as calls:
            self.se_index.force_batch_sync()
            self.assert_index_called(calls, "delete", [self.partner.id])
            self.assertFalse(self.partner_binding.exists())

    def test_batch_sync_not_exportable(self):
        for state in (
            "to_recompute",
            "recomputing",
            "invalid_data",
            "done",
            "deleting",
        ):
            self.partner_binding.state = state
            with self.se_adapter.mocked_calls() as calls:
                self.se_index.batch_sync()
                self.assertEqual(self.partner_binding.state, state)
                self.assertEqual(calls, [])

    def test_batch_sync_deletable(self):
        self.partner_binding.state = "to_delete"
        with self.se_adapter.mocked_calls() as calls:
            self.se_index.batch_sync()
            self.assert_index_called(calls, "delete", [self.partner.id])
            self.assertFalse(self.partner_binding.exists())

    def test_batch_sync_exportable(self):
        self.partner_binding.state = "to_export"
        with self.se_adapter.mocked_calls() as calls:
            self.se_index.batch_sync()
            self.assert_index_called(calls, "index", [self.partner_binding.data])
            self.assertEqual(self.partner_binding.state, "done")

    @mute_logger("odoo.addons.connector_search_engine.models.se_binding")
    def test_missing_record_to_recompute(self):
        # following case should not occure (as unlink will change the binding state)
        # but in case of weird action like sql delete we want to make it stronger
        self.partner_binding.state = "to_recompute"
        self.partner_binding.res_id = 999999999
        self.partner_binding.recompute_json()
        self.assertEqual(self.partner_binding.state, "to_delete")

    def test_clear_index(self):
        with self.se_adapter.mocked_calls() as calls:
            self.se_index.clear_index()
            self.assertEqual(len(calls), 1)
            self.assertEqual(calls[0]["index"], self.se_index)
            self.assertEqual(calls[0]["method"], "clear")

    def test_recompute_json_with_error_solve(self):
        # If something was to check but it's now good,
        # the state should be back to normal
        self.partner_binding.state = "invalid_data"
        self.partner_binding.error = "Something wrong with data"
        self.partner_binding.recompute_json()
        self.assertEqual(self.partner_binding.state, "to_export")
        self.assertEqual(self.partner_binding.error, "")

    @mute_logger("odoo.addons.connector_search_engine.models.se_binding")
    def test_recompute_json_missing_record_key(self):
        with mock.patch.object(
            self.model_serializer, "serialize", return_value={"name": "Foo"}
        ):
            self.partner_binding.recompute_json()
            self.assertEqual(self.partner_binding.state, "invalid_data")
            self.assertEqual(
                self.partner_binding.error,
                "The key 'id' is missing in the data",
            )

    def test_life_cycle(self):
        self.partner_binding.state = "done"
        # we mark the partner to update
        self.partner._se_mark_to_update()
        self.assertEqual(self.partner_binding.state, "to_recompute")
        # we launch the job scheduled every 5 minutes to recompute
        # bindings to recompute
        with trap_jobs() as trap:
            self.se_index_model.generate_batch_recompute_per_index()
            trap.assert_jobs_count(2)
            trap.assert_enqueued_job(
                self.se_index.batch_recompute,
                args=(False,),
                kwargs={},
                properties=dict(
                    identity_key=identity_exact,
                ),
            )
            trap.assert_enqueued_job(
                self.partner_binding.recompute_json,
                args=(),
                kwargs={},
            )
        # the binding is now in to_export
        self.assertEqual(self.partner_binding.state, "to_export")

        # we launch the job scheduled every 5 minutes to sync bindings
        # with the search engine
        # In our case, the binding is in to_export, so it should be exported
        with trap_jobs() as trap:
            self.se_index_model.generate_batch_sync_per_index()
            trap.assert_jobs_count(2)
            trap.assert_enqueued_job(
                self.se_index.batch_sync,
                args=(False,),
                kwargs={},
                properties=dict(
                    identity_key=identity_exact,
                ),
            )
            trap.assert_enqueued_job(
                self.partner_binding.export_record,
                args=(),
                kwargs={},
            )

        # the binding is now in done
        self.assertEqual(self.partner_binding.state, "done")

        # if we unlink the partner, the binding should be deleted on the next
        # batch sync
        self.partner.unlink()

        # we launch the job scheduled every 5 minutes to sync bindings
        # with the search engine
        # In our case, the binding is in to_delete, so it should be deleted
        with trap_jobs() as trap:
            self.se_index_model.generate_batch_sync_per_index()
            trap.assert_jobs_count(2)
            trap.assert_enqueued_job(
                self.se_index.batch_sync,
                args=(False,),
                kwargs={},
                properties=dict(
                    identity_key=identity_exact,
                ),
            )
            trap.assert_enqueued_job(
                self.partner_binding.delete_record,
                args=(),
                kwargs={},
            )
        self.assertFalse(self.partner_binding.exists())
