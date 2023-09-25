# Copyright 2013 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from collections import defaultdict
from typing import List

from odoo import _, api, fields, models

from odoo.addons.queue_job.job import identity_exact

from ..tools.adapter import SearchEngineAdapter
from ..tools.serializer import ModelSerializer
from ..tools.validator import DefaultJsonValidator, JsonValidator

_logger = logging.getLogger(__name__)


class SeIndex(models.Model):
    _name = "se.index"
    _description = "Se Index"

    __slots__ = ("_se_adapter", "_model_serializer", "_json_validator")

    name = fields.Char(compute="_compute_name", store=True)
    custom_tech_name = fields.Char(
        help="Take control of index technical name. "
        "The final index name is still computed and contains in any case: "
        "backend index name prefix and language if given. "
        "If no custom name is provided, model's normalized name will be used."
    )
    backend_id = fields.Many2one(
        "se.backend", string="Backend", required=True, ondelete="cascade"
    )
    lang_id = fields.Many2one("res.lang", string="Lang", required=False)
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        domain=lambda self: self._model_id_domain(),
        ondelete="cascade",
    )
    serializer_type = fields.Selection([])
    batch_exporting_size = fields.Integer(
        default=1000, help="Batch size for exporting element"
    )
    batch_recomputing_size = fields.Integer(
        default=50, help="Batch size for recomputing element"
    )
    config_id = fields.Many2one(
        comodel_name="se.index.config",
        string="Config",
        help="Index configuration record",
    )
    binding_ids = fields.One2many("se.binding", "index_id", "Binding")
    color = fields.Integer(string="Color Index", compute="_compute_count_binding")
    count_done = fields.Integer(compute="_compute_count_binding")
    count_pending = fields.Integer(compute="_compute_count_binding")
    count_error = fields.Integer(compute="_compute_count_binding")

    @api.depends("binding_ids.state")
    def _compute_count_binding(self):
        res = defaultdict(lambda: defaultdict(int))
        data = self.env["se.binding"].read_group(
            [
                ("index_id", "in", self.ids),
            ],
            ["index_id", "state"],
            groupby=["index_id", "state"],
            lazy=False,
        )
        for item in data:
            res[item["index_id"][0]][item["state"]] = item["__count"]

        def get(index_id, states):
            return sum([res[index_id][state] for state in states])

        for record in self:
            record.count_done = get(record.id, ["done"])
            record.count_pending = get(
                record.id,
                [
                    "to_recompute",
                    "recomputing",
                    "to_export",
                    "exporting",
                    "to_delete",
                    "deleting",
                ],
            )
            record.count_error = get(record.id, ["invalid_data", "recompute_error"])
            if record.count_error:
                record.color = 1
            elif record.count_pending:
                record.color = 2
            else:
                record.color = 10

    def __init__(self, env, ids=(), prefetch_ids=()):
        super().__init__(env, ids, prefetch_ids)
        self._se_adapter = None
        self._model_serializer = None
        self._json_validator = None

    @api.model
    def _model_id_domain(self):
        se_model_names = [
            x[0] for x in self.env["se.binding"]._get_indexable_model_selection()
        ]
        return [("model", "in", se_model_names)]

    _sql_constraints = [
        (
            "lang_model_uniq",
            "unique(backend_id, lang_id, model_id)",
            "Lang and model of index must be uniq per backend.",
        )
    ]

    def write(self, vals):
        res = super().write(vals)
        if "backend_id" in vals:
            for index in self:
                index._se_adapter = None
        return res

    @property
    def se_adapter(self) -> SearchEngineAdapter:
        if not self._se_adapter:
            self._se_adapter = self.backend_id.get_adapter(self)
        return self._se_adapter

    @property
    def model_serializer(self) -> ModelSerializer:
        if not self._model_serializer:
            self._model_serializer = self._get_serializer()
        return self._model_serializer

    @property
    def json_validator(self) -> JsonValidator:
        if not self._json_validator:
            self._json_validator = self._get_validator()
        return self._json_validator

    def _get_serializer(self) -> ModelSerializer:
        raise NotImplementedError

    def _get_validator(self) -> JsonValidator:
        return DefaultJsonValidator()

    @api.model
    def recompute_all_index(self, domain=None) -> None:
        if domain is None:
            domain = []
        self.search(domain).recompute_all_binding()

    def force_recompute_all_binding(self) -> None:
        self.recompute_all_binding(force_export=True)

    def recompute_all_binding(self, force_export: bool = False):
        target_models = self.mapped("model_id.model")
        for target_model in target_models:
            indexes = self.filtered(lambda r, m=target_model: r.model_id.model == m)
            indexes.binding_ids.jobify_recompute_json(force_export=force_export)

    @api.depends(
        "custom_tech_name", "lang_id", "model_id", "backend_id.index_prefix_name"
    )
    def _compute_name(self) -> None:
        for rec in self:
            if not rec.backend_id:
                # in onchange on concrete views rec is a new Id
                # so we can't calc the right name.
                rec.name = ""
            else:
                rec.name = rec._make_name()

    def _make_name(self) -> str:
        """Compute the final name of the index."""
        name = ""
        backend = self.backend_id
        tech_name = self._make_tech_name()
        if tech_name:
            if not backend.index_prefix_name:
                # index_prefix_name should be not empty
                # indeed from the UI the index_prefix_name is alway fill base on
                # tech_name
                # So if it's empty it because we have change some config using
                # server env or using dataencryption module
                # in that case we set the default value to fix everything
                backend._onchange_tech_name()
            bits = [backend.index_prefix_name, tech_name]
            if self.lang_id:
                bits.append(self.lang_id.code)
            name = "_".join(bits)
        return name

    def _make_tech_name(self) -> str:
        """Compute the main part of the name of the index."""
        tech_name = self.custom_tech_name or self.model_id.name or ""
        return self.backend_id._normalize_tech_name(tech_name)

    def force_batch_sync(self) -> None:
        self.ensure_one()
        self._jobify_batch_sync(force_export=True)

    def _jobify_batch_sync(self, force_export: bool = False) -> None:
        self.ensure_one()
        description = _("Prepare a batch synchronization of index '%s'") % self.name
        self.with_delay(
            description=description, identity_key=identity_exact
        ).batch_sync(force_export)

    def _jobify_batch_recompute(self, force_export: bool = False) -> None:
        self.ensure_one()
        description = _("Prepare a batch recompute of index '%s'") % self.name
        self.with_delay(
            description=description, identity_key=identity_exact
        ).batch_recompute(force_export)

    @api.model
    def generate_batch_sync_per_index(self, domain: list | None = None) -> None:
        """Generate a job for each index to sync.

        This method is usually called by a cron. It will generate a job for each
        index to sync. The sync will export the bindings marked as to_export.
        and will delete the bindings marked as to_delete.
        """
        if domain is None:
            domain = []
        for record in self.search(domain):
            record._jobify_batch_sync()

    @api.model
    def generate_batch_recompute_per_index(self, domain: list | None = None) -> None:
        """Generate a job for each index to recompute.

        This method is usually called by a cron. It will generate a job for each
        index to recompute. The recompute process will recompute the bindings
        marked as to_recompute.
        """
        if domain is None:
            domain = []
        for record in self.search(domain):
            record._jobify_batch_recompute()

    def _get_domain_for_recomputing_binding(self, force_export: bool = False) -> list:
        """Return the domain to use to find the bindings to recompute."""
        states = ["to_recompute"]
        if force_export:
            states.append("recomputing")
        return [("index_id", "=", self.id), ("state", "in", states)]

    def batch_recompute(self, force_export: bool = False) -> None:
        """Recompute all the bindings of the index marked as to_recompute."""
        self.ensure_one()
        domain = self._get_domain_for_recomputing_binding(force_export)
        bindings = self.env["se.binding"].search(domain)
        bindings_count = len(bindings)
        for batch in bindings._batch(self.batch_recomputing_size):
            description = _(
                "Recompute %(processing_count)d records of %(total_count)d "
                "for index '%(index_name)s'"
            ) % {
                "processing_count": len(batch),
                "total_count": bindings_count,
                "index_name": self.name,
            }
            batch.write({"state": "recomputing"})
            batch.with_delay(description=description).recompute_json()

    def _get_domain_for_exporting_binding(self, force_export: bool = False):
        """Return the domain to use to find the bindings to export."""
        states = ["to_export"]
        if force_export:
            states.extend(["done", "exporting"])
        return [("index_id", "=", self.id), ("state", "in", states)]

    def _batch_export(self, force_export: bool = False) -> None:
        """Export all the bindings of the index marked as to_export."""
        self.ensure_one()
        domain = self._get_domain_for_exporting_binding(force_export)
        bindings = self.env["se.binding"].search(domain)
        bindings_count = len(bindings)
        for batch in bindings._batch(self.batch_exporting_size):
            description = _(
                "Export %(processing_count)d records of %(total_count)d "
                "for index '%(index_name)s'"
            ) % dict(
                processing_count=len(batch),
                total_count=bindings_count,
                index_name=self.name,
            )
            batch.write({"state": "exporting"})
            batch.with_delay(description=description).export_record()

    def _get_domain_for_deleting_binding(self, force_export: bool = False) -> list:
        """Get the domain to search the bindings to delete."""
        states = ["to_delete"]
        if force_export:
            states.append("deleting")
        return [("index_id", "=", self.id), ("state", "in", states)]

    def _batch_delete(self, force_export: bool = True) -> None:
        """Delete all the bindings of the index marked as to_delete."""
        self.ensure_one()
        domain = self._get_domain_for_deleting_binding(force_export)
        bindings = self.env["se.binding"].search(domain)
        bindings_count = len(bindings)
        for batch in bindings._batch(self.batch_exporting_size):
            description = _(
                "Delete %(processing_count)d obsolete records of %(total_count)d "
                "for index '%(index_name)s'",
            ) % dict(
                processing_count=len(batch),
                total_count=bindings_count,
                index_name=self.name,
            )
            batch.write({"state": "deleting"})
            batch.with_delay(description=description).delete_record()

    def batch_sync(self, force_export: bool = False) -> None:
        self.ensure_one()
        self._batch_export(force_export=force_export)
        self._batch_delete(force_export=force_export)

    def clear_index(self) -> None:
        self.ensure_one()
        adapter = self.se_adapter
        adapter.clear()

    def _get_settings(self) -> dict:
        """
        Override this method is sub modules in order to pass the adequate
        settings (like Facetting, pagination, advanced settings, etc...)
        """
        self.ensure_one()
        return {}

    @api.model
    def export_all_settings(self) -> None:
        self.search([]).export_settings()

    def export_settings(self) -> None:
        self.ensure_one()
        adapter = self.se_adapter
        adapter.settings()

    def reindex(self) -> None:
        """Reindex records according."""
        self.ensure_one()
        adapter = self.se_adapter
        adapter.reindex()

    def resynchronize_all_bindings(self):
        """Force sync between Odoo records and index records.

        This method will iter on all item in the index of the search engine
        if the corresponding binding do not exist on odoo it will create a job
        that delete all this obsolete items.
        You should not use this method for day to day job, it's only an helper
        for recovering your index after corruption.
        You can also drop index but this will introduce downtime, so it's
        better to force a resynchronization"""
        for index in self:
            item_ids = []
            adapter = self.se_adapter
            binding_model = self.env[index.model_id.model]
            for index_record in adapter.each():
                ext_id = adapter._get_odoo_id_from_index_data(index_record)
                binding = binding_model.browse(ext_id).exists()
                if not binding:
                    item_ids.append(ext_id)
            index.with_delay().delete_obsolete_item(item_ids)

    def delete_obsolete_item(self, item_ids: List[int]):
        self.se_adapter.delete(item_ids)
        return f"Deleted ids : {item_ids}"
