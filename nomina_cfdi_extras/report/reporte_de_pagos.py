# -*- coding: utf-8 -*-

from odoo import models,api
from collections import defaultdict


class ReportPago(models.AbstractModel):
    _name = 'report.nomina_cfdi_extras.report_payslip_batches_pagos2'
    _description = 'Reporte de Pagos'

    def slip_by_line(self, batche):
        slip_lines = batche.slip_ids.filtered(lambda x: x.state!='cancel').mapped('line_ids')
        slip_lines = slip_lines.sorted(lambda x: x.salary_rule_id.sequence)
        lines_by_code = defaultdict(float)
        sequence_dict = {}
        for line in slip_lines:
            if (line.code, line.salary_rule_id.name) not in sequence_dict:
                sequence_dict.update({(line.code, line.salary_rule_id.name): line.salary_rule_id.sequence})
            lines_by_code[(line.salary_rule_id.sequence, line.code, line.salary_rule_id.name)] += line.total
        
        items = [(seq,code,name) for seq,code,name in sorted(lines_by_code.keys(), key=lambda x: x[0])]
        return [items,lines_by_code]

    @api.model
    def _get_report_values(self, docids, data=None):
        paclingslip_batches = self.env['hr.payslip.run'].browse(docids)
        
        return {
            'doc_ids': docids,
            'doc_model': 'hr.payslip.run',
            '_slip_by_line':self.slip_by_line,
            'docs': paclingslip_batches,
            }
