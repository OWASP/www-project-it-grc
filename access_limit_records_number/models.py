from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError, AccessError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.translate import _


class BaseLimitRecordsNumber(models.Model):
    _name = "base.limit.records_number"
    _description = "Restrictions for number of records"
    _inherits = {"base.automation": "action_rule_id"}

    action_rule_id = fields.Many2one(
        "base.automation", "Base Automation", required=True, ondelete="cascade"
    )
    max_records = fields.Integer(string="Maximum Records")
    domain = fields.Char(string="Domain", default="[]")

    @api.model
    def default_get(self, default_fields):
        res = super(BaseLimitRecordsNumber, self).default_get(default_fields)
        res["trigger"] = "on_create_or_write"
        res["state"] = "code"
        res["code"] = "env['base.limit.records_number'].verify_table()"
        return res

    @api.model
    def verify_table(self):
        """ Get parameters and verify. Raise exception if limit """
        model_name = self.env.context["active_model"]
        for rule in self.search([("model_id.model", "=", model_name)]):
            records_count = self.env[model_name].search_count(safe_eval(rule.domain))
            if records_count > rule.max_records:
                raise ValidationError(
                    _(
                        'Maximimum allowed records in table "%(model_name)s" is %(max_records)s, while after this update you would have %(records_count)s'
                    )
                    % {
                        "model_name": rule.model_id.name,
                        "max_records": rule.max_records,
                        "records_count": records_count,
                    }
                )

    @api.model
    def set_max_records(self, xmlid, max_records):
        rule = self.env.ref(xmlid)
        rule.max_records = max_records
