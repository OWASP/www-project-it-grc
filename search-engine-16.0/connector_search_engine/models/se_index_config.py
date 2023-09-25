# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import json

from odoo import api, fields, models

from odoo.addons.base_sparse_field.models.fields import Serialized


# TODO: this part is copied from Elasticsearch but should stay in base module
class SeIndexConfig(models.Model):

    _name = "se.index.config"
    _inherit = ["mail.thread"]
    _description = "Elasticsearch index configuration"

    name = fields.Char(required=True)
    body = Serialized(required=True, default={})
    # This field is used since no widget exists to edit a serialized field
    # into the web fontend
    body_str = fields.Text(
        compute="_compute_body_str",
        inverse="_inverse_body_str",
        default="{}",
        tracking=True,
    )

    @api.depends("body")
    def _compute_body_str(self):
        for rec in self:
            rec.body_str = json.dumps(rec.body)

    def _inverse_body_str(self):
        for rec in self:
            rec.body = json.loads(rec.body_str or "{}")
