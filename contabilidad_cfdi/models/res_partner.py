# -*- coding: utf-8 -*-
from odoo import fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    tipo_proveedor = fields.Selection(
        selection=[('04', _('04 - Proveedor nacional')),
                   ('05', _('05 - Proveedor extranjero')),
                   ('15', _('15 - Proveedor global')),],
        string=_('Tipo de proveedor'),
    )

    tipo_operacion = fields.Selection(
        selection=[('03', _('03 - Provisión de servicios profesionales')),
                   ('06', _('06 - Arrendamientos')),
                   ('85', _('85 - Otros')),],
        string=_('Tipo de operación'),
    )

    pais_diot = fields.Many2one('catalogos.pais_diot', string='Pais')