# Copyright 2022 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from lxml import etree

from odoo import api, fields, models

if TYPE_CHECKING:
    from .se_binding import SeBinding
    from .se_index import SeIndex


SMART_BUTTON = """
<button class="oe_stat_button"
       name="open_se_binding"
       icon="fa-list-ul"
       type="object"
       attrs="{'invisible': [('count_se_binding_total', '=', 0)]}">
       <div class="o_field_widget o_stat_info">
            <field name="count_se_binding_total" invisible="1"/>
            <span class="o_stat_value">
                <i attrs="{'invisible': [
                    '|',
                    ('count_se_binding_pending', '>', 0),
                    ('count_se_binding_error', '>', 0)
                   ]}"
                   class="fa fa-thumbs-o-up text-success o_column_title"
                   aria-hidden="true"> :
                    <field name="count_se_binding_done"/>
                </i>
                <i attrs="{'invisible': [
                    '|',
                    ('count_se_binding_pending', '=', 0),
                    ('count_se_binding_error', '>', 0)
                   ]}"
                   class="fa fa-spinner text-warning" aria-hidden="true"> :
                    <field name="count_se_binding_pending"/>
                </i>
                <i attrs="{'invisible': [('count_se_binding_error', '=', 0)]}"
                   class="fa fa-exclamation-triangle text-danger" aria-hidden="true"> :
                    <field name="count_se_binding_error"/>
                </i>
            </span>
            <span>Index</span>
       </div>
</button>"""


class SeIndexableRecord(models.AbstractModel):
    _name = "se.indexable.record"
    _description = "Mixin that make record indexable in a search engine"
    _se_indexable = True

    se_binding_ids = fields.One2many(
        string="Seacrh Engine Bindings",
        comodel_name="se.binding",
        compute="_compute_binding_ids",
    )
    count_se_binding_total = fields.Integer(compute="_compute_count_binding")
    count_se_binding_done = fields.Integer(compute="_compute_count_binding")
    count_se_binding_pending = fields.Integer(compute="_compute_count_binding")
    count_se_binding_error = fields.Integer(compute="_compute_count_binding")

    def _compute_binding_ids(self) -> None:
        binding_model = self.env["se.binding"]
        values = {
            read["res_id"][0]: read["ids"]
            for read in binding_model.read_group(
                domain=[
                    ("res_model", "=", self._name),
                    ("res_id", "in", self.ids),
                ],
                fields=["ids:array_agg(id)"],
                groupby=["res_id"],
            )
        }
        for record in self:
            record.se_binding_ids = binding_model.browse(values.get(record.id, []))

    def _get_count_per_state(self):
        res = defaultdict(lambda: defaultdict(int))
        data = self.env["se.binding"].read_group(
            [
                ("res_id", "in", self.ids),
                ("res_model", "=", self._name),
            ],
            ["res_id", "state"],
            groupby=["res_id", "state"],
            lazy=False,
        )
        map_state = {
            "done": "done",
            "to_recompute": "pending",
            "recomputing": "pending",
            "to_export": "pending",
            "exporting": "pending",
            "to_delete": "pending",
            "deleting": "pending",
            "invalid_data": "error",
            "recompute_error": "error",
        }
        for item in data:
            res[item["res_id"]][map_state[item["state"]]] += item["__count"]
        return res

    def _compute_count_binding(self):
        res = self._get_count_per_state()
        for record in self:
            record.count_se_binding_done = res[record.id]["done"]
            record.count_se_binding_pending = res[record.id]["pending"]
            record.count_se_binding_error = res[record.id]["error"]
            record.count_se_binding_total = (
                res[record.id]["done"]
                + res[record.id]["pending"]
                + res[record.id]["error"]
            )

    def _get_bindings(self, indexes: SeIndex = None) -> SeBinding:
        domain = [
            ("res_model", "=", self._name),
            ("res_id", "in", self.ids),
        ]
        if indexes:
            domain.append(("index_id", "in", indexes.ids))
        return self.env["se.binding"].search(domain)

    def _add_to_index(self, indexes: SeIndex) -> SeBinding:
        """Add the record to the index.

        It will create a binding for each record that is not already
        binded to the index and mark the others to be updated.

        :param index: The index where the record should be added
        :return: The binding recordset
        """
        bindings = self._get_bindings(indexes)
        bindings.filtered(lambda s: s.state == "to_delete").write(
            {"state": "to_recompute"}
        )
        if bindings:
            todo = self - bindings.record
        else:
            todo = self
        vals_list = [
            {
                "index_id": index.id,
                "res_id": record.id,
                "res_model": self._name,
            }
            for record in todo
            for index in indexes
        ]
        return bindings | self.env["se.binding"].create(vals_list)

    def _remove_from_index(self, indexes: SeIndex) -> None:
        """Remove the record from the index.

        It will mark the binding to be deleted.
        Once the data will be removed from the index, the binding will be
        deleted.
        """
        bindings = self._get_bindings(indexes)
        bindings.write({"state": "to_delete"})

    def _se_mark_to_update(self, indexes: SeIndex | None = None) -> None:
        """Mark the record to be updated in the index."""
        bindings = self._get_bindings(indexes)
        bindings.write({"state": "to_recompute"})

    def unlink(self):
        bindings = self._get_bindings()
        bindings.write(
            {
                "state": "to_delete",
                "res_id": False,
            }
        )
        return super().unlink()

    @api.model
    def _get_view(self, view_id=None, view_type="form", **options):
        arch, view = super()._get_view(view_id=view_id, view_type=view_type, **options)
        if view_type == "form" and self.env.user.has_group(
            "connector_search_engine.group_connector_search_engine_user"
        ):
            button_box = arch.xpath("//div[@name='button_box']")
            if button_box:
                button_box[0].append(etree.fromstring(SMART_BUTTON))
        return arch, view

    def open_se_binding(self):
        action = self.env.ref("connector_search_engine.se_binding_action").read()[0]
        action["domain"] = [("res_model", "=", self._name), ("res_id", "in", self.ids)]
        action["context"] = "{'hide_res_model': True}"
        return action
