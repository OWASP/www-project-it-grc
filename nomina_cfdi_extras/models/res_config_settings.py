# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    numoer_de_retardos_x_falta = fields.Integer("Numoer de retardos x falta")
    riesgo_de_trabajo=fields.Many2one('hr.leave.type',related='company_id.leave_type_rie_id', string='Riesgo de trabajo',readonly=False)
    enfermedad_general=fields.Many2one('hr.leave.type',related='company_id.leave_type_enf_id', string='Enfermedad general',readonly=False)
    maternidad=fields.Many2one('hr.leave.type',related='company_id.leave_type_mat_id', string='Maternidad',readonly=False)

    falta_just_con =fields.Many2one('hr.leave.type',related='company_id.leave_type_fjc', string='Falta justificada con sueldo',readonly=False)
    falta_just_sin =fields.Many2one('hr.leave.type',related='company_id.leave_type_fjs', string='Falta justifica sin sueldo',readonly=False)
    falta_injustificada =fields.Many2one('hr.leave.type',related='company_id.leave_type_fi', string='Falta injustificada',readonly=False)
    falta_retardo =fields.Many2one('hr.leave.type',related='company_id.leave_type_fr', string='Falta por retardo',readonly=False)
    vacaciones = fields.Many2one('hr.leave.type',related='company_id.leave_type_vac', string='Vacaciones',readonly=False)
    festivo_doble =fields.Many2one('hr.leave.type',related='company_id.leave_type_dfes', string='Festivo doble',readonly=False)
    festivo_triple =fields.Many2one('hr.leave.type',related='company_id.leave_type_dfes3', string='Festivo triple',readonly=False)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            numoer_de_retardos_x_falta=int(params.get_param('nomina_cfdi_extras.numoer_de_retardos_x_falta', 0)),
        )
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('nomina_cfdi_extras.numoer_de_retardos_x_falta', self.numoer_de_retardos_x_falta)
        return res
    
