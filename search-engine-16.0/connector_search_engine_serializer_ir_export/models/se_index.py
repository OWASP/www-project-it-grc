# Copyright 2023 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from ..tools.serializer import JsonifySerializer


class SeIndex(models.Model):
    _inherit = "se.index"

    serializer_type = fields.Selection(selection_add=[("ir_exports", "Exporter")])
    exporter_id = fields.Many2one(
        "ir.exports",
        string="Exporter",
        compute="_compute_exporter_id",
        readonly=False,
        store=True,
    )
    model_name = fields.Char(related="model_id.model")

    @api.constrains("serializer_type", "exporter_id")
    def _check_need_exporter(self):
        for record in self:
            if record.serializer_type == "ir_exports" and not record.exporter_id:
                raise ValidationError(
                    _("Exporter is needed when using 'ir_exports' as serializer")
                )

    @api.depends("serializer_type", "model_id")
    def _compute_exporter_id(self):
        for record in self:
            # reset exporter_id if needed
            if (
                record.serializer_type == "ir_exports"
                and record.exporter_id
                and record.exporter_id.resource != record.model_id.model
                or record.serializer_type != "ir_exports"
            ):
                record.exporter_id = False

    def _get_serializer(self):
        if self.serializer_type == "ir_exports":
            parser = self.exporter_id.get_json_parser()
            return JsonifySerializer(parser)
        else:
            return super()._get_serializer()
