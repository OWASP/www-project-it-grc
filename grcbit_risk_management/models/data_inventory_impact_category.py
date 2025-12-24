# -*- coding: utf-8 -*-

from odoo import fields, models, _


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

