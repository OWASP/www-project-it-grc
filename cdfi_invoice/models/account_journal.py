# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
import pytz


# put POSIX 'Etc/*' entries at the end to avoid confusing users - see bug 1086728
_tzs = [(tz, tz) for tz in sorted(pytz.all_timezones, key=lambda tz: tz if not tz.startswith('Etc/') else '_')]
def _tz_get(self):
    return _tzs

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    forma_pago_id  =  fields.Many2one('catalogo.forma.pago', string='Forma de pago')
    codigo_postal = fields.Char("Código Postal")
    tz = fields.Selection(_tz_get, string='Zona horaria', default=lambda self: self._context.get('tz'))
    serie_diario = fields.Char("Serie")
