# Copyright 2023 Akretion (https://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, tools
from odoo.tools import frozendict


class IrActions(models.Model):
    _inherit = "ir.actions.actions"

    @tools.ormcache("model_name", "self.env.lang")
    def _get_bindings(self, model_name):
        res = super()._get_bindings(model_name)
        model = self.env[model_name]
        if hasattr(model, "_se_indexable") and model._se_indexable and "action" in res:
            res = dict(res)
            res["action"] = tuple(
                list(res["action"])
                + [
                    self.env["ir.actions.actions"]._for_xml_id(
                        "connector_search_engine.action_recompute_se_index"
                    )
                ]
            )
            res = frozendict(res)
        return res
