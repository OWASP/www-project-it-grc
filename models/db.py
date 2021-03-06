# -*- coding: utf-8 -*-
import datetime
# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
#from _typeshed import FileDescriptor
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
             pool_size=configuration.get('db.pool_size'),
             migrate_enabled=configuration.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'


# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

auth.settings.actions_disabled.append('register')
auth.settings.actions_disabled.append('request_reset_password')
auth.settings.actions_disabled.append('retrieve_username')
auth.settings.actions_disabled.append('profile')
auth.settings.actions_disabled.append('change_password')
auth.settings.actions_disabled.append('retrieve_password')

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

#--------------------------------------------------------------------------

db.define_table('risk_classification',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('risk_treatment',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('department',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('responsible', 'string', label=T('Responsible')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('process_type',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('system_type',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('maturity_level',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('m_level', 'integer', label=T('Level'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('process',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('p_owner', 'string', label=T('Owner')),
    Field('p_file', 'upload', label=T('Flow Diagram')),
    Field('process_type_id', 'reference process_type', label=T('Process Type')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('objective_type',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('company',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('mision', 'text', label=T('Mision')),
    Field('vision', 'text', label=T('Vision')),
    Field('c_value', 'text', label=T('Values')),
    Field('security_requirement', 'text', label=T('Security Requirement')),
    Field('framework_used', 'text', label=T('Framework Used')),
    Field('product_service', 'text', label=T('Product/Service')),
    Field('c_file', 'upload', label=T('File')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('impact_level',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('i_level', 'string', label=T('Level'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('probability_level',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('p_level', 'string', label=T('Level'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('risk_level',
    Field('impact_level_id', 'reference impact_level', label=T('Impact Level')),
    Field('probability_level_id', 'reference probability_level', label=T('Probability Level')),
    Field('grc_name', 'string', label=T('Name')),
    Field('r_level', 'string', label=T('Risk Level')),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('company_objective',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('objective_type_id', 'reference objective_type', label=T('Objective Type')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('benchmark',
    Field('grc_name', 'string', label=T('Version'), ),
    Field('description', 'text', label=T('Description')),
    Field('bench_file', 'upload', label=T('File')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('bench_control_objective',
    Field('benchmark_id','reference benchmark', label=T('Benchmark')),
    Field('control_number', 'string', label=T('ID')),
    Field('grc_name', 'string', label=T('Control Objective')),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s %s %s %s %s' % (r.benchmark_id.grc_name, '|', r.control_number, '|', r.grc_name)
    )

db.define_table('strategic_risk_analysis',
    Field('description', 'text', label=T('Description')),
    Field('r_date', 'date', default=request.now, label=T('Date'), requires = IS_DATE(format=('%d/%m/%Y'))),
    Field('evidence', 'upload', label=T('Evidence')), #uploadfolder=os.path.join(request.folder,'uploads')),
    Field('consequence','text', label=T('Consequence')),
    Field('r_level', 'string', label=T('Level'), ),
    Field('r_owner', 'string', label=T('Owner')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s %s %s' % (r.id, '|', r.description)
    )
db.strategic_risk_analysis.r_level.requires=IS_IN_SET(['Low (Bajo)', 'Moderate (Moderado)', 'High (Alto)', 'Critical (Critico)'])

db.define_table('risk_analysis_classification',
    Field('strategic_risk_analysis_id', 'reference strategic_risk_analysis', label=T('Risk'), notnull=True),
    Field('risk_classification_id', 'reference risk_classification', label=T('Risk Classification'), notnull=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s %s %s %s %s' % (r.id, '|', r.strategic_risk_analysis_id.description, '|', r.risk_classification_id.grc_name)
    )

db.define_table('risk_analysis_objective',
    Field('strategic_risk_analysis_id', 'reference strategic_risk_analysis', label=T('Risk'), notnull=True),
    Field('company_objective_id', 'reference company_objective', label=T('Organisational Objective'), notnull=True),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s %s %s %s %s' % (r.id, '|', r.strategic_risk_analysis_id.description, '|', r.company_objective_id.grc_name)
    )

db.define_table('system_asset',
    Field('grc_name', 'string', label=T('Name'), unique=True),
    Field('description', 'text', label=T('Description')),
    Field('s_owner', 'string', label=T('Owner')),
    Field('s_file', 'upload', label=T('Arquitecture Diagram')),
    Field('system_type_id', 'reference system_type', label=T('System Type')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('compliance_requirement',
    Field('grc_name', 'string', label=T('Nanme')),
    Field('grc_version', 'string', label=T('Version')),
    Field('description', 'text', label=T('Description')),
    Field('compliance_file', 'upload', label=T('File')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s %s %s' % (r.grc_name, ' | ', r.grc_version)
    )

db.define_table('data_classification',
    Field('grc_name', 'string', label=T('Name')),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('data_inventory',
    Field('grc_name', 'string', label=T('Name')),
    Field('description', 'text', label=T('Description')),
    Field('data_classification_id', 'reference data_classification', label=T('Data Classification')),
    Field('data_owner', 'string', label=T('Data Owner')),
    Field('retention_time', 'integer', label=T('Retention Time (Years)')),
    Field('security_requirements', 'text', label=T('    ')),   
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

db.define_table('data_inventory_compliance',
    Field('data_inventory_id', 'reference data_inventory', label=T('Data Asset')),
    Field('compliance_requirement_id', 'reference compliance_requirement', label=T('Compliance Requirement')),
    Field('description', 'text', label=T('Description')),
    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
    Field('write_date', 'datetime', label=T('Write Date')),
    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
    format=lambda r: '%s' % (r.grc_name)
    )

#db.define_table('control_catalog',
#    Field('grc_name', 'string', label=T('Name'), unique=True),
#    Field('description', 'text', label=T('Description')),
#    Field('benchmark_id', 'reference benchmark', label=T('Benchmark')),
#    Field('implementation_guide', 'text', label=T('Implementation Guide')),
#    Field('audit_guide', 'text', label=T('Audit Guide')),
#    Field('create_date', 'datetime', label=T('Create Date'), default= datetime.datetime.now() ),
#    Field('write_date', 'datetime', label=T('Write Date')),
#    Field('risk_analyst_approval', 'boolean', label=T('Risk Analyst (Approval)'), default='F'),
#    Field('risk_manager_approval', 'boolean', label=T('Risk Manager (Approval)'), default='F'),
#    Field('risk_analyst_log', 'string', label=T('Risk Analyst (LOG)')),
#    Field('risk_manager_log', 'string', label=T('Risk Manager (LOG)')),
#    format=lambda r: '%s' % (r.grc_name)
#    )











db.define_table('grc_settings',
    Field('grc_language', 'string', label=T('Language')),
    Field('grc_name', 'string', label=T('Company Name')),
    )
db.grc_settings.grc_language.requires = IS_IN_SET(['English', 'Spanish'])

#db.TipoTratamientoRiesgo.Color.requires= IS_IN_SET(['Rosa (Pink)', 'Purpura (Purple)', 'Amarillo (Yellow)', 'Azul (Blue)', 'Naranja (Orange)', 'Gris (Gray)', 'Rojo Indio (Indian Red)', 'Salmon (Salmon)', 'Salmon Oscuro (Dark Salmon)'])
#db.TipoTratamientoRiesgo.Nombre.requires=IS_NOT_IN_DB(db, db.TipoTratamientoRiesgo.Nombre)
#table for risk type catalog
#db.define_table('risk_type',
#    Field('grc_name', 'string', label=T('NAME')),
#    Field('description', 'text', label=T('DESCRIPTION')),
#    format=lambda r: '%s' % (r.grc_name)
#    )
#db.risk_type.grc_name.requires=IS_NOT_IN_DB(db, db.risk_type.grc_name)
#table to ser basic configurations
#db.define_table('configuration_grc',
#    Field('language_grc', 'string', label=T('LANGUAGE')),
#    Field('organization_grc', 'string', label=T('ORGANIZATION NAME')),
#    )
#db.configuration_grc.language_grc.requires=IS_IN_SET(['Espanol','English'])
'''
#table to set email configurations
db.define_table('email',
    Field('server_email', 'string', label=T('SERVER')),
    Field('sender_email', 'string', label=T('SENDER')),
    Field('login_email', 'string', label=T('LOGIN')),
    Field('tls_email', 'boolean', label=T('TLS')),
    )
'''
