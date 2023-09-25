# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json

from odoo import api, fields, models
from odoo.tools import human_size


class SeBinding(models.AbstractModel):
    _inherit = "se.binding"

    data_size = fields.Char(
        string="Index record size",
        compute="_compute_data_size",
        store=True,
        help="Computed size of the index. "
        "Algolia limits record size to 10KB "
        "and exports fail if your record exceeds the quota.",
    )

    @api.depends("data")
    def _compute_data_size(self):
        for rec in self:
            rec.data_size = human_size(rec._get_bytes_size())

    def _get_bytes_size(self):
        return len(json.dumps(self.data or {}))
