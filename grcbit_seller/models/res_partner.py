# -*- coding: utf-8 -*-
import logging
import re

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, AccessError

_logger = logging.getLogger(__name__)

class ResPartnerGRC(models.Model):
    _inherit = 'res.partner'

    client_system = fields.Char(string="Client system name")
    state = fields.Selection([
        ('new','New'),
        ('activate','Activate'),
        ('inactivate','Inactivate'),
    ], string="Status", default='new')
    activate_date = fields.Date(string="Activate date")
    db_postgres_port = fields.Char(string="DB Postgres Port (5432)") # de 1000 a 5000
    # db_ssh_port = fields.Char(string="DB SSH Port")
    postgres_pwd = fields.Char(string="Postgres Password")
    grc_web_port = fields.Char(string="GRC Web Port (8069)") #de 5000 a 9000
    # grc_ssh_port = fields.Char(string="GRC SSH Port")
    grc_container_id = fields.Char(string="GRC Container ID")
    psql_container_id = fields.Char(string="PSQL Container ID")
    xdr_index_container = fields.Char(string="XDR Indexer Container ID")
    xdr_server_container = fields.Char(string="XDR Server Container ID")
    xdr_dash_container = fields.Char(string="XDR Dashboard Container ID")

    xdr_indexer_port = fields.Char(string="XDR Indexer Port (9200)") #de 9000 a 13000
    xdr_dashboard_port = fields.Char(string="XDR Dashboard Port (5601)") # de 13000 a 17000
    xdr_dashboard_port2 = fields.Char(string="XDR Dashboard Port (5602)") # de 9000 a 11000

    xdr_manager_port1 = fields.Char(string="XDR Manager Port (1514)") #de 17000 a 21000
    xdr_manager_port2 = fields.Char(string="XDR Manager Port (1515)") #de 21000 a 25000
    xdr_manager_port3 = fields.Char(string="XDR Manager Port (514/udp)") #de 21000 a 25000
    xdr_manager_port4 = fields.Char(string="XDR Manager Port (55000)") #de 21000 a 25000

    is_admin = fields.Boolean(string="is admin", compute="_get_group")

    @api.depends()
    def _get_group(self):
        for rec in self:
            flag = self.env.user.has_group('grcbit_seller.group_admin_seller')
            
            rec.is_admin = flag

    def just_range(self, field, min_value, max_value):
        for rec in self:
            if re.search("\d+", field):
                if int(field) >= min_value and int(field) <= max_value:
                    return True
                else:
                    raise ValidationError("Valor '%s' invalido, debe estar en un rango de %s a %s" % (field, min_value, max_value))
            else:
                raise ValidationError("Los puertos deben ser solo digitos. Valor '%s' incorrecto" % field)
            
    def write(self,vals):
        res = super(ResPartnerGRC, self).write(vals)
        self.just_range(self.db_postgres_port, 1000, 5000)
        self.just_range(self.grc_web_port, 5000, 9000)
        self.just_range(self.xdr_indexer_port, 9000, 13000)
        self.just_range(self.xdr_dashboard_port, 13000, 17000)
        self.just_range(self.xdr_dashboard_port2, 9000, 11000)
        self.just_range(self.xdr_manager_port1, 17000, 21000)
        self.just_range(self.xdr_manager_port2, 21000, 25000)
        self.just_range(self.xdr_manager_port3, 25000, 29000)
        self.just_range(self.xdr_manager_port4, 29000, 33000)
        return res


    # @api.model
    # def fields_get(self, allfields=None, attributes=None):
    #     fields = super().fields_get(allfields=allfields, attributes=attributes)

    #     public_fields = {field_name: description for field_name, description in fields.items()}
    #     _logger.info("#####################"+str(fields.items()))

    #     return public_fields



class XDRManagerPort(models.Model):
    _name = 'xdr.manager.port'

    name = fields.Char(string="Port")
    partner_id = fields.Many2one('res.partner', string="Partner")
