# -*- coding: utf-8 -*-
import logging
import re
import random
import string
import base64
import dns.resolver

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, AccessError

_logger = logging.getLogger(__name__)

class ResPartnerGRC(models.Model):
    _inherit = 'res.partner'

    client_system = fields.Char(string="Client system name")
    state = fields.Selection([
        ('pending','Pending'),
        ('approved','Approved'),
        ('active','Active'),
        ('inactive','Inactive'),
        ('reactive','Reactive'),
    ], string="Status", default=lambda x : x.get_state_bygroup())
    activate_date = fields.Date(string="Activate date")
    db_postgres_port = fields.Char(string="DB Postgres Port (5432)", default= lambda x: x._set_default_port('db_postgres_port', int(3000), int(3250))) # de 3000 a 3250
    xdr_pwd_b64 = fields.Char(string="XDR Basic Base64", compute="convert_xdr_pwd", store=True)
    api_b64 = fields.Char(string="API Base64", compute="convert_api_b64", store=True)
    postgres_pwd = fields.Char(string="Postgres/ZTrust Password", default=lambda x:x._default_password('postgres'))
    xdr_pwd = fields.Char(string="XDR Password", default=lambda x:x._default_password('xdr'))
    grc_web_port = fields.Char(string="GRC Web Port (8069)", default= lambda x: x._set_default_port('grc_web_port', int(3250), int(3500))) #de 3250 a 3500
    grc_container_id = fields.Char(string="GRC Container ID")
    psql_container_id = fields.Char(string="PSQL Container ID")
    xdr_index_container = fields.Char(string="XDR Indexer Container ID")
    xdr_server_container = fields.Char(string="XDR Server Container ID")
    xdr_dash_container = fields.Char(string="XDR Dashboard Container ID")

    xdr_indexer_port = fields.Char(string="XDR Indexer Port (9200)",default=lambda c: c._set_default_port('xdr_indexer_port',int(3500),int(3750))) #de 3500 a 3750
    xdr_dashboard_port = fields.Char(string="XDR Dashboard Port (5601)", default= lambda x: x._set_default_port('xdr_dashboard_port', int(3750), int(4000))) # de 3750 a 4000
    xdr_dashboard_port2 = fields.Char(string="XDR Dashboard Port (5602)", default= lambda x: x._set_default_port('xdr_dashboard_port2', int(4000), int(4250))) # de 4000 a 4250

    xdr_manager_port1 = fields.Char(string="XDR Manager Port (1514)", default= lambda x: x._set_default_port('xdr_manager_port1', int(4250), int(4500))) #de 4250 a 4500
    xdr_manager_port2 = fields.Char(string="XDR Manager Port (1515)", default= lambda x: x._set_default_port('xdr_manager_port2', int(4500), int(4750))) #de 4500 a 4750
    xdr_manager_port3 = fields.Char(string="XDR Manager Port (514/udp)", default= lambda x: x._set_default_port('xdr_manager_port3', int(4750), int(5000))) #de 4750 a 5000
    xdr_manager_port4 = fields.Char(string="XDR Manager Port (55000)", default= lambda x: x._set_default_port('xdr_manager_port4', int(5000), int(5250))) #de 5000 a 5250

    #ZITI PORTS
    ziti_controller_port1 = fields.Char(string="Ziti Controller Port (1280)", default= lambda x: x._set_default_port('ziti_controller_port1', int(5250), int(5500))) # de 5250 a 5500 
    xiti_controller_port2 = fields.Char(string="Ziti Controller Port (6262)", default= lambda x: x._set_default_port('xiti_controller_port2', int(5500), int(5750))) # de 5500 a 5750 
    ziti_edge_router1 = fields.Char(string="Ziti Edge Router (3022)", default= lambda x: x._set_default_port('ziti_edge_router1', int(5750), int(6000))) # de 5750 a 6000 
    ziti_edge_router2 = fields.Char(string="Ziti Edge Router (10080)", default= lambda x: x._set_default_port('ziti_edge_router2', int(6000), int(6250))) # de 6000 a 6250 
    ziti_console = fields.Char(string="Ziti Console (8443)", default= lambda x: x._set_default_port('ziti_console', int(6250), int(6500))) # de 6250 a 6500 
    xdr_zt = fields.Char(string="XDR ZT", default= lambda x: x._set_default_port('xdr_zt', int(6500), int(6750))) #6500 a 6750
    dns_domain = fields.Char(string="DNS Domain")
    dns_domain_check = fields.Boolean(string="Correct DNS Domain")
    is_openziti = fields.Boolean(string="OpenZiti", default=True)

    xdr_ends = fields.Selection([
        ('zero','0'),
        ('up25','Up to 25'),
        ('up50','Up to 50'),
        ('up100','Up to 100'),
        ('up250','Up to 250'),
        ('up500','Up to 500'),
    ], string="XDR Endpoints", default="zero")
    zt_serv = fields.Selection([
        ('zero','0'),
        ('up25','Up to 25'),
        ('up50','Up to 50'),
        ('up100','Up to 100'),
        ('up250','Up to 250'),
        ('up500','Up to 500'),
    ], string="ZTrust Endpoints", default="zero")
    network = fields.Char(string="Network")
    ztrust_console = fields.Char(string="ZTrust Console")
    ztrust_router = fields.Char(string="ZTrust Router")
    ztrust_controller = fields.Char(string="ZTrust Controller")
    reseller_create = fields.Many2one('res.users', string="Reseller", default=lambda s: s.self.env.user)
    dns_subdomain = fields.Char(string="DNS SubDomain")

    zt_tunnel_cont = fields.Char(string="ZT Tunnel Container ID")
    xdr_tunnel_cont = fields.Char(string="XDR Tunnel Container ID")
    url_grc = fields.Char(string="URL GRC")
    url_xdr_ztrust = fields.Char(string="URL XDR ZTrust")
    url_zt_ztrust = fields.Char(string="URL ZT ZTrust")
    url_xdr = fields.Char(string="URL XDR")
    url_zt = fields.Char(string="URL ZT")
    jwt_key_client = fields.Char(string="JWT Key Client")
    jwt_key_support = fields.Char(string="JWT Key Support")
    agent_url = fields.Char(string="Agent XDR URL")
    email_sent = fields.Boolean(string="Email Sent", default=False)
    token_xdr_url = fields.Char(string="Token XDR URL")

    #Container limits
    grc_cpu = fields.Char(string="GRC CPU", default="2")
    grc_ram = fields.Char(string="GRC RAM", default="2")
    xdr_cpu = fields.Char(string="XDR CPU", default="4")
    xdr_ram = fields.Char(string="XDR RAM", default="4")
    zt_cpu = fields.Char(string="ZT CPU", default="4")
    zt_ram = fields.Char(string="ZT RAM", default="4") 
    update_limits = fields.Boolean(string="Update Limits", default=False)
    xdr_endpoints = fields.Integer(string="XDR Endpoints")
    ztrust_services = fields.Integer(string="ZTrust Services")
    alert_enable_xdr = fields.Boolean(string="Alert Enable XDR")
    alert_enable_zt = fields.Boolean(string="Alert Enable ZT")
    is_demo = fields.Boolean(string="Demo", default=False)
    custom_lang = fields.Selection([
        ('en','English'),
        ('es','Spanish')], string="Language", default="es")

    #SSH
    ssh_zt_console = fields.Char(string="SSH ZT Console", default=lambda r: r._set_default_port('ssh_zt_console', int(2000), int(2250)))
    ssh_zt_controller = fields.Char(string="SSH ZT Controller", default=lambda r: r._set_default_port('ssh_zt_controller', int(2250), int(2500)))
    xdr_indexer = fields.Char(string="XDR Indexer", default=lambda r: r._set_default_port('xdr_indexer', int(2500), int(2750)))
    xdr_manager = fields.Char(string="XDR Manager", default=lambda r: r._set_default_port('xdr_manager', int(2750), int(3000)))
    xdr_zt_v1 = fields.Char(string="XDR Ztrust V1", default=lambda r: r._set_default_port('xdr_zt_v1', int(9443), int(9693)))
    xdr_balancer = fields.Char(string="XDR Balancer", default=lambda r: r._set_default_port('xdr_balancer', int(1750), int(2000)))
    websocket = fields.Char(string="WebSocket", default=lambda r: r._set_default_port('websocket', int(6750), int(7000)))

    xdr_node = fields.Selection([
        ('single_mode','single-node'),
        ('multi_node','multi-node'),
    ], string="XDR node")
    url_server = fields.Char(string="URL Server")
    ip_server = fields.Char(string="IP Server")
    
    @api.depends('xdr_pwd')
    def convert_xdr_pwd(self):
        for rec in self:
            if rec.xdr_pwd:
                text = 'admin:'+rec.xdr_pwd
                b = base64.b64encode(bytes(text, 'utf-8')) # bytes
                base64_str = b.decode('utf-8') # convert bytes to string
                rec.xdr_pwd_b64 = base64_str

    @api.depends('xdr_pwd')
    def convert_api_b64(self):
        for rec in self:
            if rec.xdr_pwd:
                text = 'wazuh-wui:'+rec.xdr_pwd
                b = base64.b64encode(bytes(text, 'utf-8')) # bytes
                base64_str = b.decode('utf-8') # convert bytes to string
                rec.api_b64 = base64_str


    @api.onchange('xdr_ends','xdr_endpoints')
    def get_xdr_endpoints_value(self):
        for rec in self:
            temp = 0
            limit = rec.xdr_ends
            xdr_end = rec.xdr_endpoints
            if limit == 'zero':
                temp = 0
            if limit == 'up25':
                temp = 25
            if limit == 'up50':
                temp = 50
            elif limit == 'up100':
                temp = 100
            elif limit == 'up250':
                temp = 250
            if limit == 'up500':
                temp = 500
            if xdr_end > temp:
                rec.alert_enable_xdr = True
            else:
                rec.alert_enable_xdr = False

    @api.onchange('zt_serv','ztrust_services')
    def get_zts_endpoints_value(self):
        for rec in self:
            temp = 0
            limit = rec.zt_serv
            zt_end = rec.ztrust_services
            if limit == 'zero':
                temp = 0
            if limit == 'up25':
                temp = 25
            if limit == 'up50':
                temp = 50
            elif limit == 'up100':
                temp = 100
            elif limit == 'up250':
                temp = 250
            if limit == 'up500':
                temp = 500
            if zt_end > temp:
                rec.alert_enable_zt = True
            else:
                rec.alert_enable_zt = False

    def generate_jwt(self):
        for rec in self:
            attach = self.env['ir.attachment'].sudo().create({
                'res_id': rec.id,
                'res_model': 'res.partner',
                'type': 'binary',
                'mimetype': 'application/octet-stream',
                'name': str(rec.client_system) + '.jwt',
                'index_content': 'application',
                'db_datas': rec.jwt_key_client,
            })
        return attach.id

    def sent_email_manual(self):
        for rec in self:
            if rec.state == 'active':
                mail_pool = self.sudo().env['mail.mail']
                values = {}
                values.update({
                    'subject': 'grc4ciso',
                    'partner_ids': [(6, 0, [rec.id])],
                    'body_html': 'body',
                    'res_id': rec.id,
                    'model': 'res.partner',
                    'body': """
                        <span style="font-weight:bold;">
                            Dear client,<br/>
                            This email contains the information needed to use grc4ciso platform.
                            <br/>
                            We recomend you to change the provided passwords.
                        </span><br/>
                        <div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-4"><span style="font-weight:bold;">Client:</span></div>
                                <div class="col-4">""" + str(rec.client_system)+ """</div>
                            </div>
                            <br/>
                            <div class="row" style="border: 1px solid;>
                                <div class="col-2"><span style="font-weight:bold;">GRC</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">GRC URL:</span></div>
                                <div class="col-3"><span style="text-align:right;">""" + str(rec.url_grc)+ """</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">GRC User:</span></div>
                                <div class="col-3"><span style="text-align:right;">admin@admin.com</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">GRC Password:</span></div>
                                <div class="col-3"><span style="text-align:right;">""" + str(rec.postgres_pwd)+ """</span></div>
                            </div>
                            <br/>
                            <div class="row" style="border: 1px solid;>
                                <div class="col-2"><span style="font-weight:bold;">XDR</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">XDR URL ZTrust:</span></div>
                                <div class="col-3"><span style="text-align:right;">""" + str(rec.url_xdr_ztrust)+ """</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">XDR URL:</span></div>
                                <div class="col-3"><span style="text-align:right;">""" + str(rec.url_xdr)+ """</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">XDR User:</span></div>
                                <div class="col-3"><span style="text-align:right;">admin</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">XDR Password:</span></div>
                                <div class="col-3"><span style="text-align:right;">""" + str(rec.xdr_pwd)+ """</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">XDR Agent URL:</span></div>
                                <div class="col-3"><span style="text-align:right;">""" + str(rec.agent_url)+ """</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">XDR API URL:</span></div>
                                <div class="col-3"><span style="text-align:right;">""" + str(rec.token_xdr_url)+ """</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">XDR API User:</span></div>
                                <div class="col-3"><span style="text-align:right;">wazuh-wui</span></div>
                            </div>
                            
                            <br/>
                            <div class="row" style="border: 1px solid;>
                                <div class="col-2"><span style="font-weight:bold;">ZT</span></div>
                            </div>
                            <div class="row" style="border: 1px solid;">
                                <div class="col-3"><span style="font-weight:bold;">ZT URL ZTrust:</span></div>
                                <div class="col-3"><span style="text-align:right;">""" + str(rec.url_zt_ztrust)+ """</span></div>
                            </div>
                        </div>
                    """
                })
                
                msg_id = mail_pool.sudo().create(values)
                if msg_id:
                    mail_pool.sudo().send([msg_id])
                    mail_template = self.env.ref('grcbit_seller.customer_data_email_template')
                    mail_template.sudo().attachment_ids = [(6, 0, [rec.generate_jwt()])]
                    mail_template.sudo().send_mail(self.id, raise_exception=False, force_send=True)
                    rec.email_sent = True
            else:
                return
    

    is_admin = fields.Boolean(string="is admin", compute="_get_group", store=False)
    is_consultor = fields.Boolean(string="is admin", compute="_get_group_consultor", store=False)
    _sql_constraints = [
        ('unique_name','unique(display_name)','Customer name already exist.!'),
        ('unique_dns_subdomain','unique(dns_subdomain)', 'DNS SubDomain already exist.!'),
        ('unique_db_postgres_port', 'unique(db_postgres_port)', 'DB postgres Port already exist.!'),
        ('unique_grc_web_port', 'unique(grc_web_port)', 'GRC Web Port already exist.!'),
        ('unique_xdr_indexer_port', 'unique(xdr_indexer_port)', 'XDR Indexer Port already exist.!'),
        ('unique_xdr_dashboard_port', 'unique(xdr_dashboard_port)', 'XDR Dashboard Port (5601) already exist.!'),
        ('unique_xdr_dashboard_port2', 'unique(xdr_dashboard_port2)', 'XDR Dashboard Port (5602) already exist.!'),
        ('unique_xdr_manager_port1', 'unique(xdr_manager_port1)', 'XDR Manager Port (1514) already exist.!'),
        ('unique_xdr_manager_port2', 'unique(xdr_manager_port2)', 'XDR Manager Port (1515) already exist.!'),
        ('unique_xdr_manager_port3', 'unique(xdr_manager_port3)', 'XDR Manager Port (514/udp) already exist.!'),
        ('unique_xdr_manager_port4', 'unique(xdr_manager_port4)', 'XDR Manager Port (55000) already exist.!'),
        ('unique_ziti_controller_port1', 'unique(ziti_controller_port1)', 'Ziti Controller Port (1280) already exist.!'),
        ('unique_xiti_controller_port2', 'unique(xiti_controller_port2)', 'Ziti Controller Port (6262) already exist.!'),
        ('unique_ziti_edge_router1', 'unique(ziti_edge_router1)', 'Ziti Edge Router (3022) already exist.!'),
        ('unique_ziti_edge_router2', 'unique(ziti_edge_router2)', 'Ziti Edge Router (10080) already exist.!'),
        ('unique_ziti_console', 'unique(ziti_console)', 'Ziti Console (8443) already exist.!'),
        ('unique_xdr_zt', 'unique(xdr_zt)', 'XDR ZT already exist.!'),
        ('uniquexdr_zt_v1','unique(xdr_zt_v1)', 'XDR ZT v1 already exist.!'),
        ('unique_xdr_balancer','unique(xdr_balancer)', 'XDR ZT v1 already exist.!'),
        
    ]

    def unlink(self):
        res = super(ResPartnerGRC, self).unlink()
        flag = self.env.user.has_group('grcbit_seller.group_admin_seller')
        if flag == False:
            raise ValidationError("You don't have permissions to delete clients.!")
        return res
    
    def get_state_bygroup(self):
        flag = self.env.user.has_group('grcbit_seller.group_user_seller')
        if flag == True:
            return 'approved'
        else:
            return 'pending'


    # def _set_little_princess_field(self):
    #     partners = self.env['res.partner'].search([('xdr_indexer_port','>=',3500)], order="xdr_indexer_port DESC")
    #     if not partners:
    #         return '3500'
    #     else:
    #         val = int(partners[0].xdr_indexer_port) + 1
    #         return str(val)

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
            if field == 'ziti_controller_port1':
                val = int(partners[0].ziti_controller_port1) + 1
            if field == 'xiti_controller_port2':
                val = int(partners[0].xiti_controller_port2) + 1
            if field == 'ziti_edge_router1':
                val = int(partners[0].ziti_edge_router1) + 1
            if field == 'ziti_edge_router2':
                val = int(partners[0].ziti_edge_router2) + 1
            if field == 'ziti_console':
                val = int(partners[0].ziti_console) + 1
            if field == 'xdr_zt':
                val = int(partners[0].xdr_zt) + 1
            if field == 'ssh_zt_console':
                val = int(partners[0].ssh_zt_console) + 1
            if field == 'ssh_zt_controller':
                val = int(partners[0].ssh_zt_controller) + 1
            if field == 'xdr_indexer':
                val = int(partners[0].xdr_indexer) + 1
            if field == 'xdr_manager':
                val = int(partners[0].xdr_manager) + 1
            if field == 'xdr_zt_v1':
                val = int(partners[0].xdr_zt_v1) + 1
            if field == 'xdr_balancer':
                val = int(partners[0].xdr_balancer) + 1
            if field == 'websocket':
                val = int(partners[0].websocket) + 1
            return val

    @api.onchange('db_postgres_port')
    def _onchange_is_admin_new(self):
        for rec in self:
            flag = self.env.user.has_group('grcbit_seller.group_admin_seller')
            if flag:
                rec.is_admin = True
            else:
                rec.is_admin = False

    def _get_group(self):
        for rec in self:
            flag = self.env.user.has_group('grcbit_seller.group_admin_seller')
            if flag:
                rec.is_admin = True
            else:
                rec.is_admin = False

    @api.onchange('db_postgres_port')
    def _onchange_is_consultor_new(self):
        for rec in self:
            flag = self.env.user.has_group('grcbit_seller.group_consultor_seller')
            if flag:
                rec.is_consultor = True
            else:
                rec.is_consultor = False

    def _get_group_consultor(self):
        for rec in self:
            flag = self.env.user.has_group('grcbit_seller.group_consultor_seller')
            if flag:
                rec.is_consultor = True
            else:
                rec.is_consultor = False

    def just_range(self, field, min_value, max_value):
        for rec in self:
            if field:
                if re.search("\d+", field):
                    if int(field) >= min_value and int(field) <= max_value:
                        return True
                    else:
                        raise ValidationError("Invalid value '%s', must be in the range %s to %s" % (field, min_value, max_value))
                else:
                    raise ValidationError("Ports must be digits only. Incorrect value '%s'" % field)

    @api.onchange('name')
    def _onchange_default_client_system(self):
        for rec in self:
            if rec.name:
                rec.client_system = rec.name.replace(' ','_').lower()
            else:
                rec.client_system = ''

    @api.onchange('dns_domain')
    def _onchange_default_dns_domain(self):
        for rec in self:
            if rec.name and not rec.dns_domain:
                rec.dns_domain = rec.name.replace(' ','_').lower()
            # else:
            #     rec.dns_domain = ''
        
    def write(self,vals):
        res = super(ResPartnerGRC, self).write(vals)

        self.just_range(self.ssh_zt_console, 2000, 2250)
        self.just_range(self.ssh_zt_controller, 2250, 2500)
        self.just_range(self.xdr_indexer, 2500, 2750)
        self.just_range(self.xdr_manager, 2750, 3000)
        self.just_range(self.db_postgres_port, 3000, 3250)
        self.just_range(self.grc_web_port, 3250, 3500)
        self.just_range(self.xdr_indexer_port, 3500, 3750)
        self.just_range(self.xdr_dashboard_port, 3750, 4000)
        self.just_range(self.xdr_dashboard_port2, 4000, 4250)
        self.just_range(self.xdr_manager_port1, 4250, 4500)
        self.just_range(self.xdr_manager_port2, 4500, 4750)
        self.just_range(self.xdr_manager_port3, 4750, 5000)
        self.just_range(self.xdr_manager_port4, 5000, 5250)
        self.just_range(self.ziti_controller_port1, 5250, 5500)
        self.just_range(self.xiti_controller_port2, 5500, 5750)
        self.just_range(self.ziti_edge_router1, 5750, 6000)
        self.just_range(self.ziti_edge_router2, 6000, 6250)
        self.just_range(self.ziti_console, 6250, 6500)
        self.just_range(self.xdr_zt, 6500, 6750)
        self.just_range(self.xdr_zt_v1, 9443, 9693)
        self.just_range(self.xdr_balancer, 1750, 2000)
        self.just_range(self.websocket, 6750, 7000)
        
        return res

    def has_duplicates(self, seq):
        return len(seq) != len(set(seq))

    @api.constrains('db_postgres_port','grc_web_port','xdr_indexer_port','xdr_dashboard_port','xdr_dashboard_port2','xdr_manager_port1','xdr_manager_port2','xdr_manager_port3','xdr_manager_port4','ziti_controller_port1','xiti_controller_port2','ziti_edge_router1','ziti_edge_router2','ziti_console','xdr_zt','xdr_zt_v1','xdr_balancer','websocket')
    def no_repeat_ports(self):
        ports = []
        for rec in self:
            if rec.db_postgres_port:
                ports.append(rec.db_postgres_port)
            if rec.grc_web_port:
                ports.append(rec.grc_web_port)
            if rec.xdr_indexer_port:
                ports.append(rec.xdr_indexer_port)
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
            
            if rec.ziti_controller_port1:
                ports.append(rec.ziti_controller_port1)
            if rec.xiti_controller_port2:
                ports.append(rec.xiti_controller_port2)
            if rec.ziti_edge_router1:
                ports.append(rec.ziti_edge_router1)
            if rec.ziti_edge_router2:
                ports.append(rec.ziti_edge_router2)
            if rec.ziti_console:
                ports.append(rec.ziti_console)
            if rec.xdr_zt:
                ports.append(rec.xdr_zt)
            if rec.xdr_zt_v1:
                ports.append(rec.xdr_zt_v1)
            if rec.xdr_balancer:
                ports.append(rec.xdr_balancer)
            if rec.websocket:
                ports.append(rec.websocket)
            
            
        value = self.has_duplicates(ports)
        if value == True:
            raise ValidationError("You cannot repeat ports, check your configuration.")
        
    def _default_password(self, field):
        if field == 'postgres':
            random_pass = "".join(
                random.choices(
                    string.ascii_uppercase + string.ascii_lowercase + string.digits + "%*?_", k=16,
                )
            )
        elif field == 'xdr':
            # random_pass = "".join(
            #     random.choices(
            #         string.ascii_uppercase + string.ascii_lowercase + string.digits + "@%*?-_", k=16,
            #     )
            # )
            random_pass = (
                [
                    random.choice("@$!%*?-_"),
                    random.choice(string.digits),
                    random.choice(string.ascii_lowercase),
                    random.choice(string.ascii_uppercase),
                ]
                + [
                    random.choice(
                        string.ascii_lowercase
                        + string.ascii_uppercase
                        + "@$!%*?-_"
                        + string.digits
                    ) for i in range(12)
                ]
            )

            random.shuffle(random_pass)
            random_pass = ''.join(random_pass)
        return random_pass

    @api.onchange('dns_domain','dns_subdomain')
    def is_domain_valid(self):
        for rec in self:
            subdomain = ''
            if rec.dns_subdomain:
                subdomain = rec.dns_subdomain + '.'
            
            text = subdomain + (rec.dns_domain if rec.dns_domain else '')
            try:
                if dns.resolver.resolve(text):
                    rec.dns_domain_check = True
            except:
                rec.dns_domain_check = False
        

class XDRManagerPort(models.Model):
    _name = 'xdr.manager.port'

    name = fields.Char(string="Port")
    partner_id = fields.Many2one('res.partner', string="Partner")
