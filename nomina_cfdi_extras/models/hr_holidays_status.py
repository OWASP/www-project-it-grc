# -*- coding: utf-8 -*-
from odoo import models, api
from odoo.exceptions import Warning, UserError

class HrHolidaysStatus(models.Model):
    _inherit = 'hr.leave.type'
    
   
    def unlink(self):
        for leave_type in self:
           auto_created_leaves = []
           if leave_type:
               auto_created_leaves.append(leave_type.id)
           for status in self:
               if status.id in auto_created_leaves:
                   raise UserError("No puedes borrar un registro creado automáticamente %s"%(status.name))
