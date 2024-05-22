# -*- coding: utf-8 -*-
# Author: Julien Coux
# Copyright 2016 Camptocamp SA
# Copyright 2017 Akretion - Alexis de Lattre
# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.tools.safe_eval import safe_eval
from odoo.tools import pycompat, DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError, ValidationError
import calendar
from datetime import datetime
class TrialBalanceReportWizard(models.TransientModel):
    """Trial balance report wizard."""

    _name = "trial.balance.report.wizard.cfdi"
    _description = "Trial Balance Report Wizard"
    _inherit = "contabilidad_cfdi_report_abstract_wizard"

    company_id = fields.Many2one(
        comodel_name="res.company",
        default=lambda self: self.env.user.company_id,
        required=False,
        string="Compañia",
    )
    year = fields.Selection([('2024','2024'),('2023','2023'),('2022','2022'),('2021','2021'),('2020','2020')], string="Año", required=1)
    month = fields.Selection([('01','Enero'),('02','Febrero'),('03','Marzo'),('04','Abril'),('05','Mayo'),('06','Junio'),
                              ('07','Julio'),('08','Agosto'),('09','Septiembre'),('10','Octubre'),('11', 'Noviembre'),
                              ('12','Diciembre')], string='Mes', required=1)
    fy_start_date = fields.Date(compute="_compute_fy_start_date")
    target_move = fields.Selection(
        [("posted", "All Posted Entries"), ("all", "All Entries")],
        string="Target Moves",
        required=True,
        default="posted",
    )
    hierarchy_on = fields.Selection(
        [
            ("computed", "Computed Accounts"),
            ("relation", "Child Accounts"),
            ("none", "No hierarchy"),
        ],
        string="Jerarquía",
        required=True,
        default="relation",
        help="""Computed Accounts: Use when the account group have codes
        that represent prefixes of the actual accounts.\n
        Child Accounts: Use when your account groups are hierarchical.\n
        No hierarchy: Use to display just the accounts, without any grouping.
        """,
    )
    limit_hierarchy_level = fields.Boolean("Limitar niveles")
    show_hierarchy_level = fields.Integer("Niveles a mostrar", default=1)
    hide_parent_hierarchy_level = fields.Boolean(
        "Do not display parent levels", default=False
    )
    account_ids = fields.Many2many(
        comodel_name="account.account", string="Filter accounts"
    )
    hide_account_at_0 = fields.Boolean(
        string="Hide accounts at 0",
        default=True,
        help="When this option is enabled, the trial balance will "
        "not display accounts that have initial balance = "
        "debit = credit = end balance = 0",
    )
    receivable_accounts_only = fields.Boolean()
    payable_accounts_only = fields.Boolean()
    show_partner_details = fields.Boolean()
    partner_ids = fields.Many2many(
        comodel_name='res.partner',relation='partner_trial_balance_report_wizard_contabilidad_cfdi_rel',
        string='Filter partners',
    )
    journal_ids = fields.Many2many(
        comodel_name="account.journal",relation='journal_trial_balance_report_wizard_contabilidad_cfdi_rel',
    )

    not_only_one_unaffected_earnings_account = fields.Boolean(
        readonly=True, string="Not only one unaffected earnings account"
    )

    foreign_currency = fields.Boolean(
        string="Show foreign currency",
        help="Display foreign currency for move lines, unless "
        "account currency is not setup through chart of accounts "
        "will display initial and final balance in that currency.",
    )
    cuentas_de_orden = fields.Boolean('Ocultar cuentas de orden', default=True)
    cierre_anual = fields.Boolean('Mes 13', default=False)

    @api.constrains("hierarchy_on", "show_hierarchy_level")
    def _check_show_hierarchy_level(self):
        for rec in self:
            if rec.hierarchy_on != "none" and rec.show_hierarchy_level <= 0:
                raise UserError(
                    _("The hierarchy level to filter on must be " "greater than 0.")
                )

#     @api.depends('date_from')
#     def _compute_fy_start_date(self):
#         for wiz in self.filtered('date_from'):
#             date = fields.Datetime.from_string(wiz.date_from)
#             res = self.company_id.compute_fiscalyear_dates(date)
#             wiz.fy_start_date = res['date_from']

    @api.depends('year','month')
    def _compute_fy_start_date(self):
        for wiz in self:
            if wiz.year and wiz.month:
                date = fields.Datetime.from_string(wiz.year+'-'+wiz.month+'-01')
                res = self.company_id.compute_fiscalyear_dates(date)
                wiz.fy_start_date = res["date_from"] and res["date_from"].strftime(DEFAULT_SERVER_DATE_FORMAT)
            else:
                wiz.fy_start_date = False

    @api.onchange("company_id")
    def onchange_company_id(self):
        """Handle company change."""
        count = self.env["account.account"].search_count(
            [
                ("account_type", "=", "equity_unaffected"),
                ("company_id", "=", self.company_id.id),
            ]
        )
        self.not_only_one_unaffected_earnings_account = count != 1
#         if self.company_id and self.date_range_id.company_id and \
#                 self.date_range_id.company_id != self.company_id:
#             self.date_range_id = False
        if self.company_id and self.partner_ids:
            self.partner_ids = self.partner_ids.filtered(
                lambda p: p.company_id == self.company_id or not p.company_id
            )
        if self.company_id and self.journal_ids:
            self.journal_ids = self.journal_ids.filtered(
                lambda a: a.company_id == self.company_id
            )
        if self.company_id and self.account_ids:
            if self.receivable_accounts_only or self.payable_accounts_only:
                self.onchange_type_accounts_only()
            else:
                self.account_ids = self.account_ids.filtered(
                    lambda a: a.company_id == self.company_id
                )
        res = {
            "domain": {
                "account_ids": [],
                "partner_ids": [],
#                "date_range_id": [],
                "journal_ids": [],
            }
        }
        if not self.company_id:
            return res
        else:
            res["domain"]["account_ids"] += [("company_id", "=", self.company_id.id)]
#             res["domain"]["partner_ids"] += self._get_partner_ids_domain()
            res['domain']['partner_ids'] += ['|', ('company_id', '=', self.company_id.id),('company_id', '=', False)]
#             res["domain"]["date_range_id"] += [
#                 "|",
#                 ("company_id", "=", self.company_id.id),
#                 ("company_id", "=", False),
#             ]
            res["domain"]["journal_ids"] += [("company_id", "=", self.company_id.id)]
        return res

#     @api.onchange('date_range_id')
#     def onchange_date_range_id(self):
#         """Handle date range change."""
#         self.date_from = self.date_range_id.date_start
#         self.date_to = self.date_range_id.date_end

#     
#     @api.constrains('company_id', 'date_range_id')
#     def _check_company_id_date_range_id(self):
#         for rec in self.sudo():
#             if rec.company_id and rec.date_range_id.company_id and\
#                     rec.company_id != rec.date_range_id.company_id:
#                 raise ValidationError(
#                     _('The Company in the Trial Balance Report Wizard and in '
#                       'Date Range must be the same.'))

    @api.onchange("receivable_accounts_only", "payable_accounts_only")
    def onchange_type_accounts_only(self):
        """Handle receivable/payable accounts only change."""
        if self.receivable_accounts_only or self.payable_accounts_only:
            domain = [("company_id", "=", self.company_id.id)]
            if self.receivable_accounts_only and self.payable_accounts_only:
                domain += [
                    ("account_type", "in", ("asset_receivable", "liability_payable"))
                ]
            elif self.receivable_accounts_only:
                domain += [("account_type", "=", "asset_receivable")]
            elif self.payable_accounts_only:
                domain += [("account_type", "=", "liability_payable")]
            self.account_ids = self.env["account.account"].search(domain)
        else:
            self.account_ids = None

    @api.onchange("show_partner_details")
    def onchange_show_partner_details(self):
        """Handle partners change."""
        if self.show_partner_details:
            self.receivable_accounts_only = self.payable_accounts_only = True
        else:
            self.receivable_accounts_only = self.payable_accounts_only = False

    @api.depends("company_id")
    def _compute_unaffected_earnings_account(self):
        for record in self:
            record.unaffected_earnings_account = self.env["account.account"].search(
                [
                    ("account_type", "=", "equity_unaffected"),
                    ("company_id", "=", record.company_id.id),
                ]
            )

    unaffected_earnings_account = fields.Many2one(
        comodel_name="account.account",
        compute="_compute_unaffected_earnings_account",
        store=True,
    )

    def _print_report(self, report_type):
        self.ensure_one()
        catalog_cuentas = self._context.get('catalog_cuentas')
        data = self._prepare_report_trial_balance()
        
        if report_type == "xlsx":
            report_name = "a_f_r.report_trial_balance_xlsx_contabilidad_cfdi"
            return (
                self.env["ir.actions.report"].search([("report_name", "=", report_name), ("report_type", "=", report_type)],limit=1,).report_action(self, data=data)
            )
        if report_type == "qweb-pdf":
            report_name = "contabilidad_cfdi.trial_balance"
            return (
                self.env["ir.actions.report"].search([("report_name", "=", report_name), ("report_type", "=", report_type)],limit=1,).report_action(self, data=data)
                )
        if report_type == "qweb-html":  
            if catalog_cuentas:
                report_name='contabilidad_cfdi.catalogo_cuentas'
            else:
                report_name='contabilidad_cfdi.trial_balance'
            return (self.env["ir.actions.report"].search([("report_name", "=", report_name), ("report_type", "=", report_type)],limit=1,).report_action(self, data=data))
            
        
        
#        action = self.env.ref('contabilidad_cfdi.action_report_account_account_hirarchy')
#        vals = action.read()[0]
#        context1 = vals.get('context', {})
#        if isinstance(context1, str):
#            context1 = safe_eval(context1)
#        model = self.env['report_trial_balance_contabilidad_cfdi']
#        report = self.env['report_trial_balance_contabilidad_cfdi'].create(self._prepare_report_trial_balance())
#        context1['is_cuentas_de_orden'] = self.cuentas_de_orden
#        context1['is_contabilidad_electronica'] = True
#        report.with_context(context1).compute_data_for_report()
        
#        context1['active_id'] = report.id
#        context1['active_ids'] = report.ids
#        context1['is_account_hirarchy_report'] = True
#        context1['default_fecha_ano'] = self.year
#        context1['default_fecha_mes'] = self.month
#        vals['context'] = context1
#        return vals
        

    def button_export_html(self):
        self.ensure_one()
        report_type = "qweb-html"
        return self._export(report_type)

    def button_export_pdf(self):
        self.ensure_one()
        report_type = "qweb-pdf"
        return self._export(report_type)

    def button_export_xlsx(self):
        self.ensure_one()
        report_type = "xlsx"
        return self._export(report_type)

    def _prepare_report_trial_balance(self):
        self.ensure_one()
        year = self.year or str(datetime.now().year)
        month = self.month or str(datetime.now().month)
        return {
            "wizard_id": self.id,
            "date_from": year +'-'+month +'-01',
            "date_to": year+'-'+month+'-'+str(calendar.monthrange(int(year),int(month))[1]),
            "only_posted_moves": self.target_move == "posted",
            "hide_account_at_0": self.hide_account_at_0,
            "foreign_currency": self.foreign_currency,
            "company_id": self.company_id.id,
            "account_ids": self.account_ids.ids or [],
            "partner_ids": self.partner_ids.ids or [],
            "journal_ids": self.journal_ids.ids or [],
            "fy_start_date": self.fy_start_date,
            "hierarchy_on": self.hierarchy_on,
            "limit_hierarchy_level": self.limit_hierarchy_level,
            "show_hierarchy_level": self.show_hierarchy_level,
            "hide_parent_hierarchy_level": self.hide_parent_hierarchy_level,
            "show_partner_details": self.show_partner_details,
            "unaffected_earnings_account": self.unaffected_earnings_account.id,
            "account_financial_report_lang": self.env.lang,
            "year"  : int(self.year),
            "month" : int(self.month),
        }

    def _export(self, report_type):
        """Default export is PDF."""
        
        return self._print_report(report_type)
