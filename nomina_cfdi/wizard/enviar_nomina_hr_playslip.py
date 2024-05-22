from odoo import fields,models

class EnviarNomina(models.TransientModel):
    _name='enviar.nomina'
    _description = 'Enviar nomina'

    todos = fields.Boolean(string='Rango')
    rango_de_empleados1 = fields.Integer(string='Rango de empleados')
    rango_de_empleados2 = fields.Integer(string='a')

    def envire_de_nomina(self):
        payslip_obj = self.env['hr.payslip']
        self.ensure_one()
        ctx = self._context.copy()
        payslip_id = ctx.get('payslips')
        payslips = payslip_obj.browse(payslip_id)
        if not payslips:
            return

        template = self.env.ref('nomina_cfdi.email_template_payroll', False)
        for payslip in payslips:
            if self.todos:
               if self.rango_de_empleados1 and self.rango_de_empleados2:
                  emp_no = int(payslip.employee_id.no_empleado)
                  if emp_no >= self.rango_de_empleados1 and emp_no <= self.rango_de_empleados2:
                      if not template:return
                      mail = None
                      if payslip.employee_id.correo_electronico:
                          mail = payslip.employee_id.correo_electronico
                      if not mail:
                          if payslip.employee_id.work_email:
                             mail = payslip.employee_id.work_email
                      if not mail:continue
                      template.send_mail(payslip.id, force_send=True,email_values={'email_to': mail})
            else:
               if not template:return
               mail = None
               if payslip.employee_id.correo_electronico:
                   mail = payslip.employee_id.correo_electronico
               if not mail:
                   if payslip.employee_id.work_email:
                      mail = payslip.employee_id.work_email
               if not mail:continue
               template.send_mail(payslip.id, force_send=True,email_values={'email_to': mail})
        return True
