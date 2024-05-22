# -*- coding: utf-8 -*-

from odoo import models
from collections import defaultdict

class PartnerXlsx(models.AbstractModel):
    _name = 'report.nomina_cfdi_extras.report_de_control_payslip_batch'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'report_pago'

    def generate_xlsx_report(self, workbook, data, payslip_batches):
        for batche in payslip_batches:
            slip_lines = batche.slip_ids.filtered(lambda x: x.state!='cancel').mapped('line_ids')
            slip_lines = slip_lines.sorted(lambda x: x.salary_rule_id.sequence)
            lines_by_code = defaultdict(float)
            
            sequence_dict = {}
            for line in slip_lines:
                if (line.code, line.salary_rule_id.name) not in sequence_dict:
                    sequence_dict.update({(line.code, line.salary_rule_id.name): line.salary_rule_id.sequence})
                lines_by_code[(line.salary_rule_id.sequence, line.code, line.salary_rule_id.name)] += line.total
            
            items = [(seq,code,name) for seq,code,name in sorted(lines_by_code.keys(), key=lambda x: x[0])]
                
            report_name = batche.name
            for slip in batche.slip_ids:
                if slip.state=='cancel':
                    continue
            # One sheet by each payslip batch
            sheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True})
            
            sheet.write(0, 0, 'Code', bold)
            sheet.write(0, 1, 'Descipcion', bold)
            sheet.write(0, 2, 'Total', bold)
            
            row_index = 1
            for item in items: #lines_by_code.items():
                
                #line_code_name, total
                
                code = item[1]
                description = item[2]
                
                sheet.write(row_index, 0, code)
                sheet.write(row_index, 1, description)
                sheet.write(row_index, 2, lines_by_code[item])
                row_index += 1
            
            row_index += 1
            sheet.write(row_index, 1, 'Total empleados', bold)
            sheet.write(row_index, 2, len(batche.slip_ids.filtered(lambda x: x.state!='cancel')), bold)    
                
                
                
                
