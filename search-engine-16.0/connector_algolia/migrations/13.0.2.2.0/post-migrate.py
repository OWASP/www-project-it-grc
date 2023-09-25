# Copyright 2020 Camptocamp SA (http://www.camptocamp.com).
# @author Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tools.sql import set_not_null


def migrate(cr, version):
    set_not_null(cr, "se_backend_algolia", "tech_name")
