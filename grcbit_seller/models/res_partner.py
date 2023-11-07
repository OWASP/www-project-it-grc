# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, _

class ResPartnerGRC(models.Model):
    _inherit = 'res.partner'

    client_system = fields.Char(string="Client system name")
    state = fields.Selection([
        ('new','New'),
        ('activate','Activate'),
        ('inactivate','Inactivate'),
    ], string="Status", default='new')
    activate_date = fields.Date(string="Activate date")
    db_postgres_port = fields.Char(string="DB Postgres Port")
    db_ssh_port = fields.Char(string="DB SSH Port")
    postgres_pwd = fields.Char(string="Postgres Password")
    grc_web_port = fields.Char(string="GRC Web Port")
    grc_ssh_port = fields.Char(string="GRC SSH Port")
    grc_container_id = fields.Char(string="GRC Container ID")
    psql_container_id = fields.Char(string="PSQL Container ID")
    xdr_index_container = fields.Char(string="XDR Indexer Container ID")
    xdr_server_container = fields.Char(string="XDR Server Container ID")
    xdr_dash_container = fields.Char(string="XDR Dashboard Container ID")

    xdr_manager_port = fields.One2many('xdr.manager.port', 'partner_id', string="XDR Manager Port")
    xdr_indexer_port = fields.Char(string="XDR Indexer Port")
    xdr_dashboard_port = fields.Char(string="XDR Dashboard Port")

class XDRManagerPort(models.Model):
    _name = 'xdr.manager.port'

    name = fields.Char(string="Port")
    partner_id = fields.Many2one('res.partner', string="Partner")
