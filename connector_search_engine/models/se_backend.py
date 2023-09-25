# Copyright 2013 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from typing import Type

from odoo import _, api, fields, models
from odoo.exceptions import UserError

from ..tools.adapter import SearchEngineAdapter


class SeBackend(models.Model):

    _name = "se.backend"
    _description = "Se Backend"
    _inherit = [
        "server.env.techname.mixin",
        "server.env.mixin",
    ]

    name = fields.Char(required=True)
    index_prefix_name = fields.Char(
        help="Prefix for technical indexes tech name. "
        "You could use this to change index names based on current env."
    )
    backend_type = fields.Selection(selection=[], string="Type", required=True)

    index_ids = fields.One2many("se.index", "backend_id")

    @property
    def _server_env_fields(self):
        return {"index_prefix_name": {}}

    @api.onchange("tech_name", "index_prefix_name")
    def _onchange_tech_name(self):
        res = super()._onchange_tech_name()
        if self.index_prefix_name:
            # make sure is normalized
            self.index_prefix_name = self._normalize_tech_name(self.index_prefix_name)
        else:
            self.index_prefix_name = self.tech_name
        return res

    def _handle_tech_name(self, vals):
        res = super()._handle_tech_name(vals)
        if not vals.get("index_prefix_name") and vals.get("tech_name"):
            vals["index_prefix_name"] = vals["tech_name"]
        return res

    def _get_adapter_class(self) -> Type[SearchEngineAdapter]:
        """Return the adapter class for this backend"""
        raise NotImplementedError

    def get_adapter(self, index=None) -> SearchEngineAdapter:
        """Return an instance of the adapter for this backend"""
        adapter = self._get_adapter_class()
        if adapter:
            return adapter(self, index)
        else:
            raise UserError(_("Adapter is missing for type %s") % self.backend_type)

    def action_test_connection(self):
        adapter = self.get_adapter()
        adapter.test_connection()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Connection Test Succeeded!"),
                "message": _("Everything seems properly set up!"),
                "sticky": False,
            },
        }
