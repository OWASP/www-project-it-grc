# -*- coding: utf-8 -*-

from odoo import fields, models, _, api


class DataInventory(models.Model):
    _inherit = "data.inventory"

    data_inventory_impact_category_ids = fields.One2many(
        "data.inventory.impact.category",
        "data_inventory_id",
        string=_("Impact"),
        auto_join=True,
        track_visibility="onchange",
    )


class DataInventoryImpactCategory(models.Model):
    _name = "data.inventory.impact.category"
    _description = "Data Inventory Impact Category"
    _rec_name = "impact_category_id"

    data_inventory_id = fields.Many2one(
        "data.inventory",
        string=_("Data Inventory"),
        required=True,
        ondelete="cascade",
    )
    impact_category_id = fields.Many2one(
        "impact.category",
        string=_("Impact Category"),
        required=True,
    )
    impact_level_id = fields.Many2one(
        "impact.level",
        string=_("Impact Level"),
        required=True,
    )
    description = fields.Text(string=_("Description"))

    disruption_value = fields.Float(string=_('Disruption Time Value'), help="Disruption duration numerical value.")
    disruption_unit = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ], string=_('Disruption Time Unit'), default='hours', help="Disruption duration time unit.")
    disruption_total_hours = fields.Float(string=_('Disruption Duration Total Hours'), compute='_compute_disruption_total_hours', store=True, help="Duration of the disruption.")

    @api.depends('disruption_value', 'disruption_unit')
    def _compute_disruption_total_hours(self):
        """Convert the DISRUPTION duration into total hours for easier reporting."""
        unit_factors = {
            'minutes': 1.0 / 60.0,
            'hours': 1.0,
            'days': 24.0,
            'weeks': 24.0 * 7.0,
        }
        for record in self:
            value = record.disruption_value or 0.0
            factor = unit_factors.get(record.disruption_unit, 1.0)
            record.disruption_total_hours = value * factor
