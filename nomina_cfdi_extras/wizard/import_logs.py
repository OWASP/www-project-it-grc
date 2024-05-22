# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class import_logs(models.TransientModel):
    _name = "import.logs"
    _description = 'import_logs'


    name = fields.Text(string='Log')
    
    
            

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:    
    
