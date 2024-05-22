# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from odoo.tools.mimetypes import guess_mimetype
from odoo.exceptions import Warning, UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, pycompat
from collections.abc import MutableMapping

import io, os
import base64
try:
    import xlrd
    try:
        from xlrd import xlsx
    except ImportError:
        xlsx = None
except ImportError:
    xlrd = xlsx = None

try:
    #import odf_ods_reader
    from . import odf_ods_reader
except ImportError:
    odf_ods_reader = None

FILE_TYPE_DICT = {
    'text/csv': ('csv', True, None),
    'application/vnd.ms-excel': ('xls', xlrd, 'xlrd'),
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ('xlsx', xlsx, 'xlrd >= 0.8'),
    'application/vnd.oasis.opendocument.spreadsheet': ('ods', odf_ods_reader, 'odfpy')
}
EXTENSIONS = {
    '.' + ext: handler
    for mime, (ext, handler, req) in FILE_TYPE_DICT.items()
}

class ImportarDiasWizard(models.TransientModel):
    _name = 'importar.dias.wizard.xls'
    _description = 'ImportarDiasWizard'
    
    import_file = fields.Binary("Importar",required=True)
    file_name = fields.Char("Nombre de file")
    contract_id = fields.Many2one('hr.contract', string='Contract', help="The contract for which applied this input")
    
    
    def import_xls_file(self):
        self.ensure_one()
        if not self.import_file:
            raise UserError("Please select the file first.") 
        p, ext = os.path.splitext(self.file_name)
        if ext[1:] not in ['xls','xlsx']:
            raise UserError(_("Unsupported file format \"{}\", import only supports XLS, XLSX").format(self.file_name))
        
        ctx = self._context.copy()
        active_id = ctx.get('active_id')
        active_model = ctx.get('active_model')
        if not ctx.get('active_id') or not active_model:
            return
            
        # guess mimetype from file content
        options = {u'datetime_format': u'', u'date_format': u'', u'keep_matches': False, u'encoding': u'utf-8', u'fields': [], u'quoting': u'"', u'headers': True, u'separator': u',', u'float_thousand_separator': u',', u'float_decimal_separator': u'.', u'advanced': False}
        import_file = base64.b64decode(self.import_file)
        mimetype = guess_mimetype(import_file)
        (file_extension, handler, req) = FILE_TYPE_DICT.get(mimetype, (None, None, None))
        
        result = []
        if handler:
            result = getattr(self, '_read_' + file_extension)(options,import_file)
        if not result and self.file_name:
            p, ext = os.path.splitext(self.file_name)
            if ext in EXTENSIONS:
                result = getattr(self, '_read_' + ext[1:])(options,import_file)
        if not result and req:
            raise UserError(_("Unable to load \"{extension}\" file: requires Python module \"{modname}\"").format(extension=file_extension, modname=req))
        employee_obj = self.env['hr.employee']
        employee_not_found = []
        #payslip_obj = self.env['hr.payslip']
        #field_list = payslip_obj._fields.keys()
        #default_payslip_vals = payslip_obj.default_get(field_list)
        payslip_batch = self.env[active_model].browse(active_id)
        worked_days_lines_by_payslip = {}
        other_inputs = self._context.get('other_inputs')
        for row in result:
            emp_code = row[0]
            if not emp_code:
                continue
            employee = employee_obj.search([('no_empleado','=',emp_code)],limit=1)
            if not employee:
                employee_not_found.append(emp_code)
                continue
            
            payslips = payslip_batch.slip_ids.filtered(lambda x:x.employee_id.id==employee.id)
            if not payslips:
                continue
            
            description = row[1]
            code = row[2]
            vals = {}
            if other_inputs:
                vals['amount'] = row[3]
            else:
                vals.update({'number_of_days':row[3] or '0', 'number_of_hours' : row[4] or '0'})
                
            for payslip in payslips:
                contract_id = payslip.contract_id and payslip.contract_id.id
                if not contract_id:
                    contract_ids = payslip.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
                    contract_id = contract_ids and contract_ids[0] or False
                if not contract_id:
                    contract_id = self.contract_id.id
                
                if payslip not in worked_days_lines_by_payslip:
                    worked_days_lines_by_payslip[payslip] = []
                if other_inputs:
                    worked_lines = payslip.input_line_ids.filtered(lambda x:x.code==code)
                else:    
                    worked_lines = payslip.worked_days_line_ids.filtered(lambda x:x.code==code)
                    
                if worked_lines:
                    worked_days_lines_by_payslip[payslip] += [(1, l.id, vals) for l in worked_lines]
                    #worked_lines.write({'number_of_days':no_of_days, 'number_of_hours' : no_of_hours})
                else:
                    if not contract_id:
                        raise UserError("Please select Contract. No valid contract found for employee %s."%(payslip.employee_id.name))
                    vals.update({'name':description,'code':code,'contract_id':contract_id})
                    worked_days_lines_by_payslip[payslip].append((0,0, vals))

        for payslip, worked_day_lines in worked_days_lines_by_payslip.items():
            if not worked_day_lines:
                continue
            if other_inputs:
                vls = {'input_line_ids':worked_day_lines}
            else:
                vls = {'worked_days_line_ids':worked_day_lines}
            payslip.write(vls)

        return True

    def _read_xls(self, options,import_file):
        """ Read file content, using xlrd lib """
        book = xlrd.open_workbook(file_contents=import_file)
        return self._read_xls_book(book, import_file)

    def _read_xls_book(self, book, import_file):
        sheet = book.sheet_by_index(0)
        # emulate Sheet.get_rows for pre-0.9.4
        is_header = False
        for row in map(sheet.row, range(sheet.nrows)):
            values = []
            is_first_cell = False
            first_cell_val = ''
            for cell in row:
                if cell.ctype is xlrd.XL_CELL_NUMBER:
                    is_float = cell.value % 1 != 0.0
#                     values.append(
#                         pycompat.text_type(cell.value)
#                         if is_float
#                         else pycompat.text_type(int(cell.value))
#                     )
                    cell_value = str(cell.value) if is_float else str(int(cell.value))
                    
                elif cell.ctype is xlrd.XL_CELL_DATE:
                    is_datetime = cell.value % 1 != 0.0
                    # emulate xldate_as_datetime for pre-0.9.3
                    dt = datetime.datetime(*xlrd.xldate.xldate_as_tuple(cell.value, book.datemode))
#                     values.append(
#                         dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT)
#                         if is_datetime
#                         else dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
#                     )
                    cell_value = dt.strftime(DEFAULT_SERVER_DATETIME_FORMAT) if is_datetime else dt.strftime(DEFAULT_SERVER_DATE_FORMAT)
                elif cell.ctype is xlrd.XL_CELL_BOOLEAN:
                    #values.append(u'True' if cell.value else u'False')
                    cell_value = u'True' if cell.value else u'False'
                elif cell.ctype is xlrd.XL_CELL_ERROR:
                    raise ValueError(
                        _("Error cell found while reading XLS/XLSX file: %s") %
                        xlrd.error_text_from_code.get(
                            cell.value, "unknown error code %s" % cell.value)
                    )
                else:
                    cell_value = cell.value
                if not is_first_cell:
                    first_cell_val = cell_value
                    is_first_cell = True
                values.append(cell_value)
            if not first_cell_val:
                continue    
            if not is_header:
                is_header=True
                continue
            
            if any(x for x in values if x.strip()):
                yield values

    # use the same method for xlsx and xls files
    _read_xlsx = _read_xls
    
    
    
    def _read_ods(self, options, import_file):
        """ Read file content using ODSReader custom lib """
        doc = odf_ods_reader.ODSReader(file=io.BytesIO(import_file))

        return (
            row
            for row in doc.getFirstSheet()
            if any(x for x in row if x.strip())
        )

    
    def _read_csv(self, options, import_file):
        """ Returns a CSV-parsed iterator of all empty lines in the file
            :throws csv.Error: if an error is detected during CSV parsing
            :throws UnicodeDecodeError: if ``options.encoding`` is incorrect
        """
        csv_data = self.file

        # TODO: guess encoding with chardet? Or https://github.com/aadsm/jschardet
        encoding = options.get('encoding', 'utf-8')
        if encoding != 'utf-8':
            # csv module expect utf-8, see http://docs.python.org/2/library/csv.html
            csv_data = csv_data.decode(encoding).encode('utf-8')

        csv_iterator = pycompat.csv_reader(
            io.BytesIO(csv_data),
            quotechar=str(options['quoting']),
            delimiter=str(options['separator']))

        return (
            row for row in csv_iterator
            if any(x for x in row if x.strip())
        )
    
