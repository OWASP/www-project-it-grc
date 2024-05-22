# -*- coding: utf-8 -*-
import zipfile, tempfile
import io
from odoo.tools import html_escape
import logging
import json
from odoo import http
from odoo.http import request, content_disposition, serialize_exception
_logger = logging.getLogger(__name__)


class BinaryCDFIInvoice(http.Controller):

    @http.route(['/payroll/download_document/<int:rec_id>'], type='http', auth="public")
    def download_document(self, rec_id=None, *args, **kw):
        try:
            if rec_id:
                payslip = request.env['hr.payslip.run'].browse(int(rec_id))
                allowed_extension = ['.xml', '.pdf']
                filename = payslip.name.lower().replace(' ', '_') + '.zip'
                slips = payslip.slip_ids
                stream = io.BytesIO()
                with zipfile.ZipFile(stream, 'w') as zfile:
                    for slip in slips:
                        docs = request.env['ir.attachment'].search(
                            ['&', ('res_model', '=', 'hr.payslip'), ('res_id', '=', slip.id)])
                        for doc in docs:
                            if any(doc.name.endswith(ext) for ext in allowed_extension):
                                binary_stream = request.env['ir.binary']._get_stream_from(doc, 'raw')
                                zfile.writestr(binary_stream.download_name, binary_stream.read(),
                                     compress_type=zipfile.ZIP_DEFLATED)

                content = stream.getvalue()  # Cf Todo: this is bad
                headers = [
                    ('Content-Type', 'zip'),
                    ('X-Content-Type-Options', 'nosniff'),
                    ('Content-Length', len(content)),
                    ('Content-Disposition', content_disposition(filename))
                ]
                return request.make_response(content, headers)
            return request.not_found()
        except Exception as e:
            _logger.exception("Error while generating report %s", filename)
            se = serialize_exception(e)
            error = {"code": 200, "message": "Odoo Server Error", "data": se}
            return request.make_response(html_escape(json.dumps(error)))
