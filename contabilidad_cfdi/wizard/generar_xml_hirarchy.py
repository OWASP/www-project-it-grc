
from odoo import api, models, fields,_
import requests
from odoo.exceptions import UserError
from datetime import datetime
import base64
import json
import logging
from lxml import etree as ET
_logger = logging.getLogger(__name__)

class GenerarXmlHirarchyWizard(models.TransientModel):
    _name = 'generar.xml.hirarchy.wizard'
    
    fecha_mes = fields.Selection([('01', 'Enero'), ('02', 'Febrero'), ('03', 'Marzo'), ('04', 'Abril'), ('05', 'Mayo'), ('06', 'Junio'),
                                    ('07', 'Julio'), ('08', 'Agosto'), ('09', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre'), ('12', 'Diciembre')],
                                   string='Mes', store=True)
    fecha_ano = fields.Selection([('2024', '2024'),('2023', '2023'),('2022','2022'),('2021', '2021'),('2020','2020')],
                                   string='Año', store=True)
    procesa_nivel = fields.Char(string='Nivel a procesar', store=True, default='2')
    tipo_de_reporte = fields.Selection([('Catalogo de cuentas','Catalogo de cuentas'),('Balance mensual', 'Balance mensual')],string='Tipo de reporte')
    tipoenvio = fields.Selection([('N', 'Normal'), ('C', 'Complementaria')],
                                   string='Tipo de envío', default='N')
    cierre_anual = fields.Boolean('Mes 13', default=False)
    fechamodbal = fields.Date('Fecha de modifcación')

    @api.model
    def default_get(self, fields_list):
        res = super(GenerarXmlHirarchyWizard, self).default_get(fields_list)
        ctx = self._context.copy()
        if ctx.get('catalog_cuentas'):
            res['tipo_de_reporte'] = 'Catalogo de cuentas'
        else:
            res['tipo_de_reporte'] = 'Balance mensual'
        if ctx.get('default_fecha_mes'):
            try:
                res['fecha_mes'] = ctx.get('default_fecha_mes')
            except Exception:
                pass
        if ctx.get('default_fecha_ano'):
            try:
                res['fecha_ano'] = ctx.get('default_fecha_ano')
            except Exception:
                pass
        return res

    def _get_hierarchy_groups(
        self, group_ids, groups_data, old_groups_ids, foreign_currency
    ):
        new_parents = False
        for group_id in group_ids:
            if groups_data[group_id]["parent_id"]:
                new_parents = True
                nw_id = groups_data[group_id]["parent_id"]
                if nw_id in groups_data.keys():
                    groups_data[nw_id]["initial_balance"] += groups_data[group_id][
                        "initial_balance"
                    ]
                    groups_data[nw_id]["debit"] += groups_data[group_id]["debit"]
                    groups_data[nw_id]["credit"] += groups_data[group_id]["credit"]
                    groups_data[nw_id]["balance"] += groups_data[group_id]["balance"]
                    groups_data[nw_id]["ending_balance"] += groups_data[group_id][
                        "ending_balance"
                    ]
                    if foreign_currency:
                        groups_data[nw_id]["initial_currency_balance"] += groups_data[
                            group_id
                        ]["initial_currency_balance"]
                        groups_data[nw_id]["ending_currency_balance"] += groups_data[
                            group_id
                        ]["ending_currency_balance"]
                else:
                    groups_data[nw_id] = {}
                    groups_data[nw_id]["initial_balance"] = groups_data[group_id][
                        "initial_balance"
                    ]
                    groups_data[nw_id]["debit"] = groups_data[group_id]["debit"]
                    groups_data[nw_id]["credit"] = groups_data[group_id]["credit"]
                    groups_data[nw_id]["balance"] = groups_data[group_id]["balance"]
                    groups_data[nw_id]["ending_balance"] = groups_data[group_id][
                        "ending_balance"
                    ]
                    if foreign_currency:
                        groups_data[nw_id]["initial_currency_balance"] = groups_data[
                            group_id
                        ]["initial_currency_balance"]
                        groups_data[nw_id]["ending_currency_balance"] = groups_data[
                            group_id
                        ]["ending_currency_balance"]
        if new_parents:
            nw_groups_ids = []
            for group_id in list(groups_data.keys()):
                if group_id not in old_groups_ids:
                    nw_groups_ids.append(group_id)
                    old_groups_ids.append(group_id)
            groups = self.env["account.group"].browse(nw_groups_ids)
            for group in groups:
                groups_data[group.id].update(
                    {
                        "id": group.id,
                        "code": group.code_prefix_start,
                        "name": group.name,
                        "parent_id": group.parent_id.id,
                        "parent_path": group.parent_path,
                        "complete_code": group.complete_code,
                        "account_ids": group.compute_account_ids.ids,
                        "type": "group_type",
                        "cuenta_sat": group.cuenta_sat or '',
                        "cuenta_tipo": group.cuenta_tipo or '',
                        "subctade": group.parent_id and group.parent_id.code_prefix_start or '',
                    }
                )
            groups_data = self._get_hierarchy_groups(
                nw_groups_ids, groups_data, old_groups_ids, foreign_currency
            )
        return groups_data

    def _get_groups_data(self, accounts_data, total_amount, foreign_currency):
        accounts_ids = list(accounts_data.keys())
        accounts = self.env["account.account"].browse(accounts_ids)
        account_group_relation = {}
        for account in accounts:
            accounts_data[account.id]["complete_code"] = (
                account.group_id.complete_code if account.group_id.id else ""
            )
            if account.group_id.id:
                if account.group_id.id not in account_group_relation.keys():
                    account_group_relation.update({account.group_id.id: [account.id]})
                else:
                    account_group_relation[account.group_id.id].append(account.id)
        groups = self.env["account.group"].browse(account_group_relation.keys())
        groups_data = {}
        for group in groups:
            groups_data.update(
                {
                    group.id: {
                        "id": group.id,
                        "code": group.code_prefix_start,
                        "name": group.name,
                        "parent_id": group.parent_id.id,
                        "parent_path": group.parent_path,
                        "type": "group_type",
                        "complete_code": group.complete_code,
                        "account_ids": group.compute_account_ids.ids,
                        "initial_balance": 0.0,
                        "credit": 0.0,
                        "debit": 0.0,
                        "balance": 0.0,
                        "ending_balance": 0.0,
                        "account_ids": group.compute_account_ids.ids,
                        "cuenta_sat": group.cuenta_sat or '',
                        "cuenta_tipo": group.cuenta_tipo or '',
                        "subctade": group.parent_id and group.parent_id.code_prefix_start or '',
                    }
                }
            )
            if foreign_currency:
                groups_data[group.id]["initial_currency_balance"] = 0.0
                groups_data[group.id]["ending_currency_balance"] = 0.0
        for group_id in account_group_relation.keys():
            for account_id in account_group_relation[group_id]:
                groups_data[group_id]["initial_balance"] += total_amount[account_id][
                    "initial_balance"
                ]
                groups_data[group_id]["debit"] += total_amount[account_id]["debit"]
                groups_data[group_id]["credit"] += total_amount[account_id]["credit"]
                groups_data[group_id]["balance"] += total_amount[account_id]["balance"]
                groups_data[group_id]["ending_balance"] += total_amount[account_id]["ending_balance"]
                if foreign_currency:
                    groups_data[group_id]["initial_currency_balance"] += total_amount[
                        account_id
                    ]["initial_currency_balance"]
                    groups_data[group_id]["ending_currency_balance"] += total_amount[
                        account_id
                    ]["ending_currency_balance"]
        group_ids = list(groups_data.keys())
        old_group_ids = list(groups_data.keys())
        groups_data = self._get_hierarchy_groups(
            group_ids, groups_data, old_group_ids, foreign_currency
        )
        return groups_data

    def _get_computed_groups_data(self, accounts_data, total_amount, foreign_currency):
        groups = self.env["account.group"].search([("id", "!=", False)])
        groups_data = {}
        for group in groups:
            len_group_code = len(group.code_prefix_start)
            groups_data.update(
                {
                    group.id: {
                        "id": group.id,
                        "code": group.code_prefix_start,
                        "name": group.name,
                        "parent_id": group.parent_id.id,
                        "parent_path": group.parent_path,
                        "type": "group_type",
                        "complete_code": group.complete_code,
                        "account_ids": group.compute_account_ids.ids,
                        "initial_balance": 0.0,
                        "credit": 0.0,
                        "debit": 0.0,
                        "balance": 0.0,
                        "ending_balance": 0.0,
                        "cuenta_sat": group.cuenta_sat or '',
                        "cuenta_tipo": group.cuenta_tipo or '',
                        "subctade": group.parent_id and group.parent_id.code_prefix_start or '',
                    }
                }
            )
            if foreign_currency:
                groups_data[group.id]["initial_currency_balance"] = 0.0
                groups_data[group.id]["ending_currency_balance"] = 0.0
            for account in accounts_data.values():
                if group.code_prefix_start == account["code"][:len_group_code]:
                    acc_id = account["id"]
                    group_id = group.id
                    groups_data[group_id]["initial_balance"] += total_amount[acc_id][
                        "initial_balance"
                    ]
                    groups_data[group_id]["debit"] += total_amount[acc_id]["debit"]
                    groups_data[group_id]["credit"] += total_amount[acc_id]["credit"]
                    groups_data[group_id]["balance"] += total_amount[acc_id]["balance"]
                    groups_data[group_id]["ending_balance"] += total_amount[acc_id][
                        "ending_balance"
                    ]
                    if foreign_currency:
                        groups_data[group_id][
                            "initial_currency_balance"
                        ] += total_amount[acc_id]["initial_currency_balance"]
                        groups_data[group_id][
                            "ending_currency_balance"
                        ] += total_amount[acc_id]["ending_currency_balance"]
        return groups_data

   
    def action_validate_xml(self):
        ctx = self._context.copy()
        data = ctx.get('data')
        show_partner_details = data["show_partner_details"]
        company_id = data["company_id"]
        partner_ids = data["partner_ids"]
        journal_ids = data["journal_ids"]
        account_ids = data["account_ids"]
        date_to = data["date_to"]
        date_from = data["date_from"]
        hide_account_at_0 = data["hide_account_at_0"]

        foreign_currency = data["foreign_currency"]
        only_posted_moves = data["only_posted_moves"]
        unaffected_earnings_account = data["unaffected_earnings_account"]
        fy_start_date = data["fy_start_date"]
        hierarchy_on = data["hierarchy_on"]
        trial_balance = []
        if ctx.get('catalog_cuentas'):
            total_amount, accounts_data, partners_data = self.env['report.contabilidad_cfdi.catalogo_cuentas']._get_data(
                account_ids,
                journal_ids,
                partner_ids,
                company_id,
                date_to,
                date_from,
                foreign_currency,
                only_posted_moves,
                show_partner_details,
                hide_account_at_0,
                unaffected_earnings_account,
                fy_start_date,
            )
            if not show_partner_details:
                for account_id in accounts_data.keys():
                    account = self.env['account.account'].search([('id', '=', account_id)])
                    accounts_data[account_id].update(
                        {
                            "initial_balance": total_amount[account_id]["initial_balance"],
                            "credit": total_amount[account_id]["credit"],
                            "debit": total_amount[account_id]["debit"],
                            "balance": total_amount[account_id]["balance"],
                            "ending_balance": total_amount[account_id]["ending_balance"],
                            "cuenta_sat": account.cuenta_sat or '',
                            "cuenta_tipo": account.cuenta_tipo or '',
                            "subctade": account.group_id.code_prefix_start or '',
                            "type": "account_type",
                        }
                    )
                    if foreign_currency:
                        accounts_data[account_id].update(
                            {
                                "ending_currency_balance": total_amount[account_id][
                                    "ending_currency_balance"
                                ],
                                "initial_currency_balance": total_amount[account_id][
                                    "initial_currency_balance"
                                ],
                            }
                        )
                if hierarchy_on == "relation":
                    groups_data = self._get_groups_data(
                        accounts_data, total_amount, foreign_currency
                    )
                    trial_balance = list(groups_data.values())
                    trial_balance += list(accounts_data.values())
                    trial_balance = sorted(trial_balance, key=lambda k: k["complete_code"])
                    for trial in trial_balance:
                        counter = trial["complete_code"].count("/")
                        if trial["type"] == 'account_type':
                           trial["level"] = counter+1
                        else:
                           trial["level"] = counter
                if hierarchy_on == "computed":
                    groups_data = self._get_computed_groups_data(
                        accounts_data, total_amount, foreign_currency
                    )
                    trial_balance = list(groups_data.values())
                    trial_balance += list(accounts_data.values())
                    trial_balance = sorted(trial_balance, key=lambda k: k["code"])
                if hierarchy_on == "none":
                    trial_balance = list(accounts_data.values())
                    trial_balance = sorted(trial_balance, key=lambda k: k["code"])
            else:
                if foreign_currency:
                    for account_id in accounts_data.keys():
                        total_amount[account_id]["currency_id"] = accounts_data[account_id][
                            "currency_id"
                        ]
                        total_amount[account_id]["currency_name"] = accounts_data[
                            account_id
                        ]["currency_name"]
        else:
            total_amount, accounts_data, partners_data = self.env['report.contabilidad_cfdi.trial_balance']._get_data(
                account_ids,
                journal_ids,
                partner_ids,
                company_id,
                date_to,
                date_from,
                foreign_currency,
                only_posted_moves,
                show_partner_details,
                hide_account_at_0,
                unaffected_earnings_account,
                fy_start_date,
            )
            if not show_partner_details:
                for account_id in accounts_data.keys():
                    accounts_data[account_id].update(
                        {
                            "initial_balance": total_amount[account_id]["initial_balance"],
                            "credit": total_amount[account_id]["credit"],
                            "debit": total_amount[account_id]["debit"],
                            "balance": total_amount[account_id]["balance"],
                            "ending_balance": total_amount[account_id]["ending_balance"],
                            "type": "account_type",
                        }
                    )
                    if foreign_currency:
                        accounts_data[account_id].update(
                            {
                                "ending_currency_balance": total_amount[account_id][
                                    "ending_currency_balance"
                                ],
                                "initial_currency_balance": total_amount[account_id][
                                    "initial_currency_balance"
                                ],
                            }
                        )
                if hierarchy_on == "relation":
                    groups_data = self._get_groups_data(
                        accounts_data, total_amount, foreign_currency
                    )
                    trial_balance = list(groups_data.values())
                    trial_balance += list(accounts_data.values())
                    trial_balance = sorted(trial_balance, key=lambda k: k["complete_code"])
                    for trial in trial_balance:
                        counter = trial["complete_code"].count("/")
                        if trial["type"] == 'account_type':
                           trial["level"] = counter+1
                        else:
                           trial["level"] = counter
                if hierarchy_on == "computed":
                    groups_data = self._get_computed_groups_data(
                        accounts_data, total_amount, foreign_currency
                    )
                    trial_balance = list(groups_data.values())
                    trial_balance += list(accounts_data.values())
                    trial_balance = sorted(trial_balance, key=lambda k: k["code"])
                if hierarchy_on == "none":
                    trial_balance = list(accounts_data.values())
                    trial_balance = sorted(trial_balance, key=lambda k: k["code"])
            else:
                if foreign_currency:
                    for account_id in accounts_data.keys():
                        total_amount[account_id]["currency_id"] = accounts_data[account_id][
                            "currency_id"
                        ]
                        total_amount[account_id]["currency_name"] = accounts_data[
                            account_id
                        ]["currency_name"]

        url=''
        company = self.env.user.company_id
        if company.proveedor_timbrado == 'multifactura':
            url = '%s' % ('http://facturacion.itadmin.com.mx/api/contabilidad')
        elif company.proveedor_timbrado == 'multifactura2':
            url = '%s' % ('http://facturacion2.itadmin.com.mx/api/contabilidad')
        elif company.proveedor_timbrado == 'multifactura3':
            url = '%s' % ('http://facturacion3.itadmin.com.mx/api/contabilidad')
        elif company.proveedor_timbrado == 'gecoerp':
            if company.modo_prueba:
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
            else:
                url = '%s' % ('https://itadmin.gecoerp.com/invoice/?handler=OdooHandler33')
        
        values = self.to_json(trial_balance)
        
        response = requests.post(url,auth=None,verify=False, data=json.dumps(values),headers={"Content-type": "application/json"})
        
#        _logger.info('something ... %s', response.text)

        json_response = response.json()
        estado_factura = json_response.get('estado_conta','')
        if not estado_factura:
           estado_factura = json_response.get('estado_factura','')
        if estado_factura == 'problemas_contabilidad' or estado_factura == 'problemas_factura':
            raise UserError(_(json_response['problemas_message']))
        if json_response.get('conta_xml'):
            
            #_logger.info("xml %s", json_response['conta_xml'])
            #_logger.info("zip %s", json_response['conta_zip'])

            #return base64.b64decode(json_response['conta_xml'])
            try:
                form_id = self.env['ir.model.data'].check_object_reference('contabilidad_cfdi', 'reporte_conta_xml_zip_download_wizard_download_form_view_itadmin')[1]
            except ValueError:
                form_id = False
            ctx.update({'default_xml_data': json_response['conta_xml'], 'default_zip_data': json_response.get('conta_zip', None),'conta_name':json_response['conta_name']})    
            return {
                'name': 'genera xml',   
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'conta.xml.zip.download',
                'views': [(form_id, 'form')],
                'view_id': form_id,
                'target': 'new',
                'context': ctx,
            }
            
        return True

    
    @api.model
    def to_json(self, total_amount):
        company = self.env.user.company_id
        if not company.archivo_cer or not company.archivo_key:
           raise UserError("No tiene cargado el certificado correctamente.")
        archivo_cer = company.archivo_cer
        archivo_key = company.archivo_key
        request_params = { 
                'informacion': {
                      'api_key': company.proveedor_timbrado,
                      'modo_prueba': company.modo_prueba,
                      'proceso': '',
                      'RFC': company.vat,
                      'Mes': self.fecha_mes,
                      'Anio': self.fecha_ano,
                      'version': '2.0',
                },
                'certificados': {
                      'archivo_cer': archivo_cer.decode("utf-8"),
                      'archivo_key': archivo_key.decode("utf-8"),
                      'contrasena': company.contrasena,
                },}
        account_lines = []
        account_obj = self.env['account.account']
        if self.tipo_de_reporte == 'Catalogo de cuentas':
            for account_id in total_amount:
                if len(account_id['cuenta_sat']) > 2:
                   account_lines.append({'SubCtaDe': account_id['subctade'] if len(account_id['subctade']) > 2 else '',
                                      'CodAgrup': account_id['cuenta_sat'],
                                      'NumCta': account_id['code'],
                                      'Desc': account_id['name'],
                                      'Nivel': account_id['level'],
                                      'Natur': account_id['cuenta_tipo']})
            request_params.update({'Catalogo':{
                         'RFC': company.vat,
                         'Mes': self.fecha_mes,
                         'Anio': self.fecha_ano,
                         'Ctas': account_lines
                       },})
            request_params['informacion'].update({'proceso': 'catalogo',})
        else:
            for account_id in total_amount:
                if len(account_id['code']) > 2:
                   account_lines.append({'NumCta': account_id['code'],
                                      'SaldoIni': round(account_id['initial_balance'],2),
                                      'Debe': account_id['debit'],
                                      'Haber': account_id['credit'],
                                      'SaldoFin': round(account_id['ending_balance'],2),
                                      })
            request_params.update({'Balanza':{
                         'RFC': company.vat,
                         'Mes': self.fecha_mes if not self.cierre_anual else '13',
                         'Anio': self.fecha_ano,
                         'TipoEnvio': self.tipoenvio,
                         'FechaModBal': self.fechamodbal,
                         'Ctas': account_lines
                       },})
            request_params['informacion'].update({'proceso': 'balanza',})

        #_logger.info(json.dumps(request_params))
        return request_params

class ContaXMLZIPDownload(models.TransientModel):
    _name = 'conta.xml.zip.download'
    
    xml_data = fields.Binary("XML File")
    zip_data = fields.Binary("Zip File")
    def download_xml_zip_file(self):
        if self._context.get('file_type','')=='zip':
            field_name = 'zip_data'
            filename = '%s.zip'%self._context.get('conta_name')
        else:
            field_name = 'xml_data'
            filename = '%s.xml'%self._context.get('conta_name')
        return {
                'type' : 'ir.actions.act_url',
                'url': "/web/content/?model="+self._name+"&id=" + str(self.id) + "&field="+field_name+"&download=true&filename="+filename,
                'target':'self',
                }   

