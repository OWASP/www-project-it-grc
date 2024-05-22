# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    leave_type_rie_id=fields.Many2one('hr.leave.type', string='Riesgo de trabajo',store=True)
    leave_type_enf_id=fields.Many2one('hr.leave.type', string='Enfermedad general',store=True)
    leave_type_mat_id=fields.Many2one('hr.leave.type', string='Maternidad',store=True)

    leave_type_fjc =fields.Many2one('hr.leave.type', string='Falta justificada con sueldo',store=True)
    leave_type_fjs =fields.Many2one('hr.leave.type', string='Falta justifica sin sueldo',store=True)
    leave_type_fi =fields.Many2one('hr.leave.type', string='Falta injustificada',store=True)
    leave_type_fr =fields.Many2one('hr.leave.type', string='Falta por retardo',store=True)
    leave_type_vac = fields.Many2one('hr.leave.type', string='Vacaciones',store=True)
    leave_type_dfes =fields.Many2one('hr.leave.type', string='Festivo doble',store=True)
    leave_type_dfes3 =fields.Many2one('hr.leave.type', string='Festivo triple',store=True)