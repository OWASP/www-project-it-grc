# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models

from ..utils import data_merge


class SeIndex(models.Model):

    _inherit = "se.index"

    def _get_settings(self):
        settings = super()._get_settings()
        if self.config_id and self.config_id.body:
            # Smart merge of settings: extend instead of override all values
            settings = data_merge(settings, self.config_id.body)
        return settings
