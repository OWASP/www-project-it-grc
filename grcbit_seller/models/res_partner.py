# -*- coding: utf-8 -*-
import logging
import re
import random
import string

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, AccessError

_logger = logging.getLogger(__name__)

class ResPartnerGRC(models.Model):
    _inherit = 'res.partner'

    client_system = fields.Char(string="Client system name")
    state = fields.Selection([
        ('new','New'),
        ('active','Active'),
        ('inactive','Inactive'),
    ], string="Status", default='new')
    activate_date = fields.Date(string="Activate date")
    db_postgres_port = fields.Char(string="DB Postgres Port (5432)", default= lambda x: x._set_default_port('db_postgres_port', int(1000), int(5000))) # de 1000 a 5000
    # db_ssh_port = fields.Char(string="DB SSH Port")
    postgres_pwd = fields.Char(string="Postgres Password", default=lambda x:x._default_password())
    grc_web_port = fields.Char(string="GRC Web Port (8069)", default= lambda x: x._set_default_port('grc_web_port', int(5000), int(9000))) #de 5000 a 9000
    # grc_ssh_port = fields.Char(string="GRC SSH Port")
    grc_container_id = fields.Char(string="GRC Container ID")
    psql_container_id = fields.Char(string="PSQL Container ID")
    xdr_index_container = fields.Char(string="XDR Indexer Container ID")
    xdr_server_container = fields.Char(string="XDR Server Container ID")
    xdr_dash_container = fields.Char(string="XDR Dashboard Container ID")

    xdr_indexer_port = fields.Char(string="XDR Indexer Port (9200)",default=lambda c: c._set_little_princess_field())# default= lambda x: x._set_default_port('xdr_indexer_port', int(9000), int(13000))) #de 9000 a 13000
    xdr_dashboard_port = fields.Char(string="XDR Dashboard Port (5601)", default= lambda x: x._set_default_port('xdr_dashboard_port', int(13000), int(17000))) # de 13000 a 17000
    xdr_dashboard_port2 = fields.Char(string="XDR Dashboard Port (5602)", default= lambda x: x._set_default_port('xdr_dashboard_port2', int(33000), int(37000))) # de 33000 a 37000

    xdr_manager_port1 = fields.Char(string="XDR Manager Port (1514)", default= lambda x: x._set_default_port('xdr_manager_port1', int(17000), int(21000))) #de 17000 a 21000
    xdr_manager_port2 = fields.Char(string="XDR Manager Port (1515)", default= lambda x: x._set_default_port('xdr_manager_port2', int(21000), int(25000))) #de 21000 a 25000
    xdr_manager_port3 = fields.Char(string="XDR Manager Port (514/udp)", default= lambda x: x._set_default_port('xdr_manager_port3', int(25000), int(29000))) #de 25000 a 29000
    xdr_manager_port4 = fields.Char(string="XDR Manager Port (55000)", default= lambda x: x._set_default_port('xdr_manager_port4', int(29000), int(33000))) #de 29000 a 33000

    is_admin = fields.Boolean(string="is admin", compute="_get_group", store=False)
    _sql_constraints = [
        ('unique_db_postgres_port', 'unique(db_postgres_port)', 'DB postgres Port already exist.!'),
        ('unique_grc_web_port', 'unique(grc_web_port)', 'GRC Web Port already exist.!'),
        ('unique_xdr_indexer_port', 'unique(xdr_indexer_port)', 'XDR Indexer Port already exist.!'),
        ('unique_xdr_dashboard_port', 'unique(xdr_dashboard_port)', 'XDR Dashboard Port (5601) already exist.!'),
        ('unique_xdr_dashboard_port2', 'unique(xdr_dashboard_port2)', 'XDR Dashboard Port (5602) already exist.!'),
        ('unique_xdr_manager_port1', 'unique(xdr_manager_port1)', 'XDR Manager Port (1514) already exist.!'),
        ('unique_xdr_manager_port2', 'unique(xdr_manager_port2)', 'XDR Manager Port (1515) already exist.!'),
        ('unique_xdr_manager_port3', 'unique(xdr_manager_port3)', 'XDR Manager Port (514/udp) already exist.!'),
        ('unique_xdr_manager_port4', 'unique(xdr_manager_port4)', 'XDR Manager Port (55000) already exist.!'),
    ]

    def _set_little_princess_field(self):
        partners = self.env['res.partner'].search([('xdr_indexer_port','>=',9000)], order="xdr_indexer_port DESC")
        if not partners:
            return 9000
        else:
            val = int(partners[0].xdr_indexer_port) + 1
            return val

    def _set_default_port(self, field, min_value, max_value):
        val = 0
        partners = self.env['res.partner'].sudo().search([(field,'>=', min_value),(field, '<=', max_value)], order="%s DESC" % field)
        if not partners:
            return min_value
        else:      
            if field == 'db_postgres_port':
                val = int(partners[0].db_postgres_port) + 1
            if field == 'grc_web_port':
                val = int(partners[0].grc_web_port) + 1
            if field == 'xdr_indexer_port':
                val = int(partners[0].xdr_indexer_port) + 1
            if field == 'xdr_dashboard_port':
                val = int(partners[0].xdr_dashboard_port) + 1
            if field == 'xdr_dashboard_port2':
                val = int(partners[0].xdr_dashboard_port2) + 1
            if field == 'xdr_manager_port1':
                val = int(partners[0].xdr_manager_port1) + 1
            if field == 'xdr_manager_port2':
                val = int(partners[0].xdr_manager_port2) + 1
            if field == 'xdr_manager_port3':
                val = int(partners[0].xdr_manager_port3) + 1
            if field == 'xdr_manager_port4':
                val = int(partners[0].xdr_manager_port4) + 1
            return val

    @api.onchange('db_postgres_port')
    def _onchange_is_admin_new(self):
        for rec in self:
            flag = self.env.user.has_group('grcbit_seller.group_admin_seller')
            rec.is_admin = flag

    def _get_group(self):
        for rec in self:
            flag = self.env.user.has_group('grcbit_seller.group_admin_seller')
            rec.is_admin = flag

    def just_range(self, field, min_value, max_value):
        for rec in self:
            if field:
                if re.search("\d+", field):
                    if int(field) >= min_value and int(field) <= max_value:
                        return True
                    else:
                        raise ValidationError("Valor '%s' invalido, debe estar en un rango de %s a %s" % (field, min_value, max_value))
                else:
                    raise ValidationError("Los puertos deben ser solo digitos. Valor '%s' incorrecto" % field)

    @api.onchange('name')
    def _onchange_default_client_system(self):
        for rec in self:
            if rec.name:
                rec.client_system = rec.name.replace(' ','_').lower()
            else:
                rec.client_system = ''
        
    def write(self,vals):
        res = super(ResPartnerGRC, self).write(vals)
        
        self.just_range(self.db_postgres_port, 1000, 5000)
        self.just_range(self.grc_web_port, 5000, 9000)
        self.just_range(self.xdr_indexer_port, 9000, 13000)
        self.just_range(self.xdr_dashboard_port, 13000, 17000)
        self.just_range(self.xdr_dashboard_port2, 33000, 37000)
        self.just_range(self.xdr_manager_port1, 17000, 21000)
        self.just_range(self.xdr_manager_port2, 21000, 25000)
        self.just_range(self.xdr_manager_port3, 25000, 29000)
        self.just_range(self.xdr_manager_port4, 29000, 33000)
        return res

    def has_duplicates(self, seq):
        return len(seq) != len(set(seq))

    @api.constrains('db_postgres_port','grc_web_port','xdr_indexer_port','xdr_dashboard_port','xdr_dashboard_port2','xdr_manager_port1','xdr_manager_port2','xdr_manager_port3','xdr_manager_port4')
    def no_repeat_ports(self):
        ports = []
        for rec in self:
            if rec.db_postgres_port:
                ports.append(rec.db_postgres_port)
            if rec.grc_web_port:
                ports.append(rec.grc_web_port )
            if rec.xdr_indexer_port:
                ports.append(rec.xdr_indexer_port )
            if rec.xdr_dashboard_port:
                ports.append(rec.xdr_dashboard_port)
            if rec.xdr_dashboard_port2:
                ports.append(rec.xdr_dashboard_port2)
            if rec.xdr_manager_port1:
                ports.append(rec.xdr_manager_port1)
            if rec.xdr_manager_port2:
                ports.append(rec.xdr_manager_port2)
            if rec.xdr_manager_port3:
                ports.append(rec.xdr_manager_port3)
            if rec.xdr_manager_port4:
                ports.append(rec.xdr_manager_port4)
            
        value = self.has_duplicates(ports)
        if value == True:
            raise ValidationError("No se puede repetir puertos, verifique su configuracion")
        
    def _default_password(self):
        random_pass = "".join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits + "@$%*?-_", k=16,
            )
        )
        return random_pass

class XDRManagerPort(models.Model):
    _name = 'xdr.manager.port'

    name = fields.Char(string="Port")
    partner_id = fields.Many2one('res.partner', string="Partner")
