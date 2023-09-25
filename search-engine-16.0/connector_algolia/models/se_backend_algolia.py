# Copyright 2013 Akretion (http://www.akretion.com)
# Raphaël Valyi <raphael.valyi@akretion.com>
# Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import fields, models


class SeBackendAlgolia(models.Model):
    _name = "se.backend.algolia"
    _inherit = [
        "se.backend.spec.abstract",
        "server.env.techname.mixin",
        "server.env.mixin",
    ]
    _description = "Algolia Backend"

    _search_engine_name = "algolia"
    _record_id_key = "objectID"

    algolia_app_id = fields.Char(string="APP ID")
    algolia_api_key = fields.Char(string="API KEY")
    # `tech_name` should come from `server.env.techname.mixin`
    # but `se.backend.spec.abstract` adds delegation inheritance
    # with `se.backend` which inherits as well from `server.env.techname.mixin`
    # hence the field is not created in this specific model table
    tech_name = fields.Char(
        related="se_backend_id.tech_name", store=True, readonly=False
    )

    @property
    def _server_env_fields(self):
        env_fields = super()._server_env_fields
        env_fields.update({"algolia_app_id": {}, "algolia_api_key": {}})
        return env_fields

    def _get_api_credentials(self):
        return {"password": self.algolia_api_key}  # pragma: no cover
