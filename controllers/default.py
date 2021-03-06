# -*- coding: utf-8 -*-
import base64
import datetime

def index():
    #-----------------------------------------------------------------------------------
    # Initial configuration
    # Change password of admin user and delete or comment these lines for production
    #db.auth_user.update_or_insert((db.auth_user.id==1),id=1, first_name="admin", last_name="admin", email="admin@email.com", username="admin", password=db.auth_user.password.validate('Password01')[0])
    #db.auth_group.update_or_insert((db.auth_group.id==1),id=1, role="admin", description="admin")
    #db.auth_membership.update_or_insert((db.auth_membership.id==1),id=1, user_id=1, group_id=1)
    #-----------------------------------------------------------------------------------
    import random
    risk_array = {}
    for i in range(0,25):
        for j in range(0,25):
            risk_array[i,j]=random.randint(0, 20)
    return dict(risk_array=risk_array)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

#--------------
#Risk Catalog
#--------------
@auth.requires_login()
def risk_classification():
    db.risk_classification.id.readable=False
    db.risk_classification.risk_manager_approval.writable=False
    db.risk_classification.risk_analyst_approval.writable=False
    db.risk_classification.risk_manager_log.writable=False
    db.risk_classification.risk_analyst_log.writable=False
    db.risk_classification.create_date.writable=False
    db.risk_classification.write_date.writable=False
    table_name = 'risk_classification'
    fields = (db.risk_classification.grc_name, db.risk_classification.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_classification, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_classification, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.risk_classification.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def risk_treatment():
    db.risk_treatment.id.readable=False
    db.risk_treatment.risk_manager_approval.writable=False
    db.risk_treatment.risk_analyst_approval.writable=False
    db.risk_treatment.risk_manager_log.writable=False
    db.risk_treatment.risk_analyst_log.writable=False
    db.risk_treatment.create_date.writable=False
    db.risk_treatment.write_date.writable=False
    table_name = 'risk_treatment'
    fields = (db.risk_treatment.grc_name, db.risk_treatment.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_treatment, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_treatment, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.risk_treatment.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def impact_level():
    db.impact_level.id.readable=False
    db.impact_level.risk_manager_approval.writable=False
    db.impact_level.risk_analyst_approval.writable=False
    db.impact_level.risk_manager_log.writable=False
    db.impact_level.risk_analyst_log.writable=False
    db.impact_level.create_date.writable=False
    db.impact_level.write_date.writable=False
    db.impact_level.grc_name.writable=False
    db.impact_level.i_level.writable=False
    table_name = 'impact_level'
    fields = (db.impact_level.grc_name, db.impact_level.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.impact_level, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.impact_level, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.impact_level.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def probability_level():
    db.probability_level.id.readable=False
    db.probability_level.risk_manager_approval.writable=False
    db.probability_level.risk_analyst_approval.writable=False
    db.probability_level.risk_manager_log.writable=False
    db.probability_level.risk_analyst_log.writable=False
    db.probability_level.create_date.writable=False
    db.probability_level.write_date.writable=False
    db.probability_level.grc_name.writable=False
    db.probability_level.p_level.writable=False
    table_name = 'probability_level'
    fields = (db.probability_level.grc_name, db.probability_level.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.probability_level, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.probability_level, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.probability_level.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def risk_level():
    db.risk_level.id.readable=False
    db.risk_level.risk_manager_approval.writable=False
    db.risk_level.risk_analyst_approval.writable=False
    db.risk_level.risk_manager_log.writable=False
    db.risk_level.risk_analyst_log.writable=False
    db.risk_level.create_date.writable=False
    db.risk_level.write_date.writable=False
    db.risk_level.impact_level_id.writable=False
    db.risk_level.probability_level_id.writable=False
    db.risk_level.grc_name.writable=False
    db.risk_level.r_level.writable=False
    table_name = 'risk_level'
    fields = (db.risk_level.grc_name, db.risk_level.description, db.risk_level.impact_level_id, db.risk_level.probability_level_id)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_level, fields=fields, links=links, searchable=True, create=False, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_level, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.risk_level.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

#---------------------
#Organization Context
#---------------------
@auth.requires_login()
def department():
    db.department.id.readable=False
    db.department.risk_manager_approval.writable=False
    db.department.risk_analyst_approval.writable=False
    db.department.risk_manager_log.writable=False
    db.department.risk_analyst_log.writable=False
    db.department.create_date.writable=False
    db.department.write_date.writable=False
    table_name = 'department'
    fields = (db.department.grc_name, db.department.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.department, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.department, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.department.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def objective_type():
    db.objective_type.id.readable=False
    db.objective_type.risk_manager_approval.writable=False
    db.objective_type.risk_analyst_approval.writable=False
    db.objective_type.risk_manager_log.writable=False
    db.objective_type.risk_analyst_log.writable=False
    db.objective_type.create_date.writable=False
    db.objective_type.write_date.writable=False
    table_name = 'objective_type'
    fields = (db.objective_type.grc_name, db.objective_type.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.objective_type, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.objective_type, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.objective_type.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def company():
    db.company.id.readable=False
    db.company.risk_manager_approval.writable=False
    db.company.risk_analyst_approval.writable=False
    db.company.risk_manager_log.writable=False
    db.company.risk_analyst_log.writable=False
    db.company.create_date.writable=False
    db.company.write_date.writable=False
    table_name = 'company'
    fields = (db.company.grc_name, db.company.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.company, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.company, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.company.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def company_objective():
    db.company_objective.id.readable=False
    db.company_objective.risk_manager_approval.writable=False
    db.company_objective.risk_analyst_approval.writable=False
    db.company_objective.risk_manager_log.writable=False
    db.company_objective.risk_analyst_log.writable=False
    db.company_objective.create_date.writable=False
    db.company_objective.write_date.writable=False
    table_name = 'company_objective'
    fields = (db.company_objective.grc_name, db.company_objective.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.company_objective, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.company_objective, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.company_objective.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def compliance_requirement():
    db.compliance_requirement.id.readable=False
    db.compliance_requirement.risk_manager_approval.writable=False
    db.compliance_requirement.risk_analyst_approval.writable=False
    db.compliance_requirement.risk_manager_log.writable=False
    db.compliance_requirement.risk_analyst_log.writable=False
    db.compliance_requirement.create_date.writable=False
    db.compliance_requirement.write_date.writable=False
    table_name = 'compliance_requirement'
    fields = (db.compliance_requirement.grc_name, db.compliance_requirement.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.compliance_requirement, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.compliance_requirement, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.compliance_requirement.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

#--------------------------------------
#Assets (IT systems, processes, data)
#--------------------------------------
@auth.requires_login()
def process_type():
    db.process_type.id.readable=False
    db.process_type.risk_manager_approval.writable=False
    db.process_type.risk_analyst_approval.writable=False
    db.process_type.risk_manager_log.writable=False
    db.process_type.risk_analyst_log.writable=False
    db.process_type.create_date.writable=False
    db.process_type.write_date.writable=False
    table_name = 'process_type'
    fields = (db.process_type.grc_name, db.process_type.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.process_type, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.process_type, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.process_type.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def system_type():
    db.system_type.id.readable=False
    db.system_type.risk_manager_approval.writable=False
    db.system_type.risk_analyst_approval.writable=False
    db.system_type.risk_manager_log.writable=False
    db.system_type.risk_analyst_log.writable=False
    db.system_type.create_date.writable=False
    db.system_type.write_date.writable=False
    table_name = 'system_type'
    fields = (db.system_type.grc_name, db.system_type.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.system_type, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.system_type, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.system_type.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def process():
    db.process.id.readable=False
    db.process.risk_manager_approval.writable=False
    db.process.risk_analyst_approval.writable=False
    db.process.risk_manager_log.writable=False
    db.process.risk_analyst_log.writable=False
    db.process.create_date.writable=False
    db.process.write_date.writable=False
    table_name = 'process'
    fields = (db.process.grc_name, db.process.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.process, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.process, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.process.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def system_asset():
    db.system_asset.id.readable=False
    db.system_asset.risk_manager_approval.writable=False
    db.system_asset.risk_analyst_approval.writable=False
    db.system_asset.risk_manager_log.writable=False
    db.system_asset.risk_analyst_log.writable=False
    db.system_asset.create_date.writable=False
    db.system_asset.write_date.writable=False
    table_name = 'system_asset'
    fields = (db.system_asset.grc_name, db.system_asset.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.system_asset, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.system_asset, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.system_asset.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def data_classification():
    db.data_classification.id.readable=False
    db.data_classification.risk_manager_approval.writable=False
    db.data_classification.risk_analyst_approval.writable=False
    db.data_classification.risk_manager_log.writable=False
    db.data_classification.risk_analyst_log.writable=False
    db.data_classification.create_date.writable=False
    db.data_classification.write_date.writable=False
    table_name = 'data_classification'
    fields = (db.data_classification.grc_name, db.data_classification.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.data_classification, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.data_classification, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.data_classification.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def data_inventory():
    db.data_inventory.id.readable=False
    db.data_inventory.risk_manager_approval.writable=False
    db.data_inventory.risk_analyst_approval.writable=False
    db.data_inventory.risk_manager_log.writable=False
    db.data_inventory.risk_analyst_log.writable=False
    db.data_inventory.create_date.writable=False
    db.data_inventory.write_date.writable=False
    table_name = 'data_inventory'
    fields = (db.data_inventory.grc_name, db.data_inventory.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.data_inventory, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.data_inventory, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.data_inventory.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def data_inventory_compliance():
    db.data_inventory_compliance.id.readable=False
    db.data_inventory_compliance.risk_manager_approval.writable=False
    db.data_inventory_compliance.risk_analyst_approval.writable=False
    db.data_inventory_compliance.risk_manager_log.writable=False
    db.data_inventory_compliance.risk_analyst_log.writable=False
    db.data_inventory_compliance.create_date.writable=False
    db.data_inventory_compliance.write_date.writable=False
    table_name = 'data_inventory_compliance'
    fields = (db.data_inventory_compliance.data_inventory_id, db.data_inventory_compliance.compliance_requirement_id, db.data_inventory_compliance.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.data_inventory_compliance, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='riskAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.data_inventory_compliance, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='auditManager') or auth.has_membership(role='auditAnalyst') or auth.has_membership(role='guest'):
        query = db.data_inventory_compliance.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))
#------------------------
#Audit & Control
#------------------------
@auth.requires_login()
def maturity_level():
    db.maturity_level.id.readable=False
    db.maturity_level.risk_manager_approval.writable=False
    db.maturity_level.risk_analyst_approval.writable=False
    db.maturity_level.risk_manager_log.writable=False
    db.maturity_level.risk_analyst_log.writable=False
    db.maturity_level.create_date.writable=False
    db.maturity_level.write_date.writable=False
    table_name = 'maturity_level'
    fields = (db.maturity_level.grc_name, db.maturity_level.description)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='auditManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.maturity_level, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.maturity_level, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='guest'):
        query = db.maturity_level.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def benchmark():
    db.benchmark.id.readable=False
    db.benchmark.risk_manager_approval.writable=False
    db.benchmark.risk_analyst_approval.writable=False
    db.benchmark.risk_manager_log.writable=False
    db.benchmark.risk_analyst_log.writable=False
    db.benchmark.create_date.writable=False
    db.benchmark.write_date.writable=False
    table_name = 'benchmark'
    fields = (db.benchmark.grc_name, db.benchmark.description, db.benchmark.bench_file)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='auditManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.benchmark, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.benchmark, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='guest'):
        query = db.benchmark.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def bench_control_objective():
    db.bench_control_objective.id.readable=False
    db.bench_control_objective.risk_manager_approval.writable=False
    db.bench_control_objective.risk_analyst_approval.writable=False
    db.bench_control_objective.risk_manager_log.writable=False
    db.bench_control_objective.risk_analyst_log.writable=False
    db.bench_control_objective.create_date.writable=False
    db.bench_control_objective.write_date.writable=False
    table_name = 'bench_control_objective'
    fields = (db.bench_control_objective.benchmark_id, db.bench_control_objective.control_number, db.bench_control_objective.grc_name)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='auditManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.bench_control_objective, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.bench_control_objective, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='guest'):
        query = db.bench_control_objective.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def strategic_risk_analysis():
    db.strategic_risk_analysis.id.readable=False
    db.strategic_risk_analysis.risk_manager_approval.writable=False
    db.strategic_risk_analysis.risk_analyst_approval.writable=False
    db.strategic_risk_analysis.risk_manager_log.writable=False
    db.strategic_risk_analysis.risk_analyst_log.writable=False
    db.strategic_risk_analysis.create_date.writable=False
    db.strategic_risk_analysis.write_date.writable=False
    table_name = 'strategic_risk_analysis'
    fields = (db.strategic_risk_analysis.description, db.strategic_risk_analysis.r_date, db.strategic_risk_analysis.r_level)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='auditManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.strategic_risk_analysis, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.strategic_risk_analysis, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='guest'):
        query = db.strategic_risk_analysis.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def risk_analysis_classification():
    db.risk_analysis_classification.id.readable=False
    db.risk_analysis_classification.risk_manager_approval.writable=False
    db.risk_analysis_classification.risk_analyst_approval.writable=False
    db.risk_analysis_classification.risk_manager_log.writable=False
    db.risk_analysis_classification.risk_analyst_log.writable=False
    db.risk_analysis_classification.create_date.writable=False
    db.risk_analysis_classification.write_date.writable=False
    table_name = 'risk_analysis_classification'
    fields = (db.risk_analysis_classification.strategic_risk_analysis_id, db.risk_analysis_classification.risk_classification_id)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='auditManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_analysis_classification, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_analysis_classification, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='guest'):
        query = db.risk_analysis_classification.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

@auth.requires_login()
def risk_analysis_objective():
    db.risk_analysis_objective.id.readable=False
    db.risk_analysis_objective.risk_manager_approval.writable=False
    db.risk_analysis_objective.risk_analyst_approval.writable=False
    db.risk_analysis_objective.risk_manager_log.writable=False
    db.risk_analysis_objective.risk_analyst_log.writable=False
    db.risk_analysis_objective.create_date.writable=False
    db.risk_analysis_objective.write_date.writable=False
    table_name = 'risk_analysis_objective'
    fields = (db.risk_analysis_objective.strategic_risk_analysis_id, db.risk_analysis_objective.company_objective_id)
    links = [lambda row: A(T('Approve'),_class='button btn btn-success',_href=URL("default",request.function, args=['approve', request.function, row.id] )), lambda row: A(T('Not Approved'),_class='button btn btn-primary',  _href=URL("default",request.function, args=['not_approve', request.function, row.id] )  )]
    if auth.has_membership(role='admin') or auth.has_membership(role='auditManager'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_analysis_objective, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=True, user_signature=True, paginate=10, maxtextlength=500))
    elif auth.has_membership(role='auditAnalyst'):
        _record_update(table_name)
        return dict(form=SQLFORM.grid(db.risk_analysis_objective, fields=fields, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    elif  auth.has_membership(role='riskOwner') or auth.has_membership(role='riskManager') or auth.has_membership(role='riskAnalyst') or auth.has_membership(role='guest'):
        query = db.risk_analysis_objective.risk_manager_approval=='T'
        return dict(form=SQLFORM.grid(query=query, fields=fields, searchable=True, create=False, deletable=False,editable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

#---------------------------------------------------------------------------------------------------
# To set basic configurations in GRC
# Load Demo Data modify current records, it is recomended to use only at the initial configuration 
#---------------------------------------------------------------------------------------------------
@auth.requires_login()
def grc_settings():
    #if auth.has_membership(role='admin') or auth.has_membership(role='riskManager'):
    if auth.has_membership(role='admin'):
        links = [lambda row: A(T('Load Demo Data'),_class='button btn btn-warning',_href=URL("grc_demo_data","_load_demo_data")) ]
        return dict(form=SQLFORM.grid(db.grc_settings, links=links, searchable=True, create=True, editable=True, deletable=False, user_signature=True, paginate=10, maxtextlength=500))
    else:
        redirect(URL('default','index'))

#-----------------------------------------------------------------------
#Function to update approval status to False if the record is edited
#-----------------------------------------------------------------------
@auth.requires_login()
def _record_update(table_name):

    if request.args(0) == 'approve':
        if table_name=='risk_classification':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_classification.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_classification.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='risk_treatment':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_treatment.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_treatment.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='department':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.department.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.department.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='objective_type':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.objective_type.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.objective_type.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='process_type':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.process_type.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.process_type.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='system_type':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.system_type.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.system_type.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='process':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.process.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.process.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='system_asset':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.system_asset.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.system_asset.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='maturity_level':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.maturity_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.maturity_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='company':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.company.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.company.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='impact_level':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.impact_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.impact_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='probability_level':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.probability_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.probability_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='risk_level':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='company_objective':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.company_objective.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.company_objective.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='compliance_requirement':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.compliance_requirement.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.compliance_requirement.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='data_classification':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.data_classification.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.data_classification.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='data_inventory':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.data_inventory.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.data_inventory.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='data_inventory_compliance':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.data_inventory_compliance.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.data_inventory_compliance.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='benchmark':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.benchmark.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.benchmark.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='bench_control_objective':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.bench_control_objective.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.bench_control_objective.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='strategic_risk_analysis':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.strategic_risk_analysis.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.strategic_risk_analysis.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='risk_analysis_classification':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_analysis_classification.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_analysis_classification.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')
        if table_name=='risk_analysis_objective':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_analysis_objective.id==request.args[len(request.args)-1]).update(risk_manager_approval='T')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_analysis_objective.id==request.args[len(request.args)-1]).update(risk_analyst_approval='T')

        _log_update( request.args[len(request.args)-1], table_name, '0', str(request.args(0))    )

    if request.args(0) == 'not_approve':
        if table_name=='risk_classification':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_classification.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_classification.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='risk_treatment':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_treatment.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_treatment.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='department':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.department.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.department.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='objective_type':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.objective_type.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.objective_type.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='process_type':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.process_type.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.process_type.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='system_type':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.system_type.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.system_type.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='process':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.process.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.process.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='system_asset':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.system_asset.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.system_asset.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='maturity_level':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.maturity_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.maturity_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='company':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.company.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.company.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='impact_level':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.impact_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.impact_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='probability_level':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.probability_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.probability_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='risk_level':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='company_objective':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.company_objective.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.company_objective.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='compliance_requirement':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.compliance_requirement.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.compliance_requirement.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='data_classification':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.data_classification.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.data_classification.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='data_inventory':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.data_inventory.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.data_inventory.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='data_inventory_compliance':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.data_inventory_compliance.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.data_inventory_compliance.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='benchmark':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.benchmark.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.benchmark.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='bench_control_objective':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.bench_control_objective.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.bench_control_objective.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='strategic_risk_analysis':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.strategic_risk_analysis.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.strategic_risk_analysis.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='risk_analysis_classification':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_analysis_classification.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_analysis_classification.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
        if table_name=='risk_analysis_objective':
            if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
                db(db.risk_analysis_objective.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            elif (auth.has_membership(role='riskAnalyst')):
                db(db.risk_analysis_objective.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')

        _log_update( request.args[len(request.args)-1], table_name, '0', str(request.args(0))    )
        
    if request.args(0) == 'edit':
        if table_name=='risk_classification':
            db(db.risk_classification.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.risk_classification.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.risk_classification.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())            
        if table_name=='risk_treatment':
            db(db.risk_treatment.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.risk_treatment.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.risk_treatment.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='department':
            db(db.department.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.department.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.department.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='process_type':
            db(db.process_type.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.process_type.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.process_type.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='system_type':
            db(db.system_type.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.system_type.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.system_type.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='process':
            db(db.process.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.process.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.process.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='system_asset':
            db(db.system_asset.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.system_asset.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.system_asset.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='maturity_level':
            db(db.maturity_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.maturity_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.maturity_level.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='objective_type':
            db(db.objective_type.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.objective_type.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.objective_type.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='company':
            db(db.company.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.company.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.company.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='impact_level':
            db(db.impact_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.impact_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.impact_level.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='probability_level':
            db(db.probability_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.probability_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.probability_level.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='risk_level':
            db(db.risk_level.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.risk_level.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.risk_level.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='company_objective':
            db(db.company_objective.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.company_objective.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.company_objective.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='benchmark':
            db(db.benchmark.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.benchmark.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.benchmark.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='bench_control_objective':
            db(db.bench_control_objective.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.bench_control_objective.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.bench_control_objective.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='strategic_risk_analysis':
            db(db.strategic_risk_analysis.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.strategic_risk_analysis.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.strategic_risk_analysis.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='risk_analysis_classification':
            db(db.risk_analysis_classification.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.risk_analysis_classification.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.risk_analysis_classification.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='risk_analysis_objective':
            db(db.risk_analysis_objective.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.risk_analysis_objective.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.risk_analysis_objective.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='compliance_requirement':
            db(db.compliance_requirement.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.compliance_requirement.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.compliance_requirement.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='data_classification':
            db(db.data_classification.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.data_classification.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.data_classification.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='data_inventory':
            db(db.data_inventory.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.data_inventory.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.data_inventory.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())
        if table_name=='data_inventory_compliance':
            db(db.data_inventory_compliance.id==request.args[len(request.args)-1]).update(risk_analyst_approval='F')
            db(db.data_inventory_compliance.id==request.args[len(request.args)-1]).update(risk_manager_approval='F')
            db(db.data_inventory_compliance.id==request.args[len(request.args)-1]).update(write_date= datetime.datetime.now())

        _log_update( request.args[len(request.args)-1], table_name, '0', str(request.args(0))    )


#---------------------------------------------------------------------------
#Function to update approval status to False(0)/True(1) and log this action
#---------------------------------------------------------------------------
@auth.requires_login()
#def _log_update(record_id='', table_name='', status='', action=''):
def _log_update(*args):
    if len(args)>0:
        record_id = args[0]
        table_name = args[1]    #'risk_classification' #str(request.get_vars['table_name'])
        status = args[2]        #str(request.get_vars['status'])
        action = args[3]        #'Approved' #str(request.get_vars['action'])
    else:
        redirect(URL('default', 'index'))

    #---------------------------------------------
    #If username or email configuration in db.py
    #---------------------------------------------
    #action = request.args(3)
    has_context_params = False

    try:
        signature = action + ',' + auth.user.username + ',' + request.client + ',' + str(request.now) #+ ',' + str(response.session_id)
    except:
        signature = action + ',' + auth.user.email + ',' + request.client + ',' + str(request.now)    #+ ',' + str(response.session_id)
      
    #-----------------------------------------------
    #context_params is to use the same http context 
    #-----------------------------------------------
    if request.args(4):
        context_params = base64.b64decode(request.args(4))
        has_context_params = True
    else:
        pass

    if table_name == 'risk_classification':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.risk_classification.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.risk_classification.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'risk_treatment':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.risk_treatment.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.risk_treatment.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'department':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.department.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.department.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'process_type':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.process_type.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.process_type.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'system_type':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.system_type.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.system_type.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'objective_type':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.objective_type.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.objective_type.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'process':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.process.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.process.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'system_asset':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.system_asset.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.system_asset.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'maturity_level':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.maturity_level.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.maturity_level.id==request.args(0)).update(risk_analyst_log=signature)    
    if table_name == 'company':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.company.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.company.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'impact_level':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.impact_level.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.impact_level.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'probability_level':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.probability_level.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.probability_level.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'risk_level':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.risk_level.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.risk_level.id==request.args(0)).update(risk_analyst_log=signature)       
    if table_name == 'company_objective':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.company_objective.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.company_objective.id==request.args(0)).update(risk_analyst_log=signature)    
    if table_name == 'benchmark':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.benchmark.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.benchmark.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'bench_control_objective':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.bench_control_objective.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.bench_control_objective.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'strategic_risk_analysis':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.strategic_risk_analysis.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.strategic_risk_analysis.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'risk_analysis_classification':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.risk_analysis_classification.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.risk_analysis_classification.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'risk_analysis_objective':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.risk_analysis_objective.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.risk_analysis_objective.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'compliance_requirement':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.compliance_requirement.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.compliance_requirement.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'data_classification':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.data_classification.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.data_classification.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'data_inventory':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.data_inventory.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.data_inventory.id==request.args(0)).update(risk_analyst_log=signature)
    if table_name == 'data_inventory_compliance':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            db(db.data_inventory_compliance.id==record_id).update(risk_manager_log=signature)
        elif (auth.has_membership(role='riskAnalyst')):
            db(db.data_inventory_compliance.id==request.args(0)).update(risk_analyst_log=signature)

    '''
    if request.args(1) == 'risk_treatment':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.risk_treatment.id==request.args(0)).update(risk_manager_log=signature)
                db(db.risk_treatment.id==request.args(0)).update(risk_manager_approval='T')
            elif request.args(2)=='0':
                db(db.risk_treatment.id==request.args(0)).update(risk_manager_log=signature)
                db(db.risk_treatment.id==request.args(0)).update(risk_manager_approval='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.risk_treatment.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.risk_treatment.id==request.args(0)).update(risk_analyst_approval='T')
            elif request.args(2)=='0':
                db(db.risk_treatment.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.risk_treatment.id==request.args(0)).update(risk_analyst_approval='F')
        if has_context_params:
            redirect(URL('risk_treatment', vars=dict(keywords=context_params)))
        else:
            redirect(URL('risk_treatment'))
            
    if request.args(1) == 'department':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.department.id==request.args(0)).update(risk_manager_log=signature)
                db(db.department.id==request.args(0)).update(risk_manager_approval='T')
            elif request.args(2)=='0':
                db(db.department.id==request.args(0)).update(risk_manager_log=signature)
                db(db.department.id==request.args(0)).update(risk_manager_approval='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.department.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.department.id==request.args(0)).update(risk_analyst_approval='T')
            elif request.args(2)=='0':
                db(db.department.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.department.id==request.args(0)).update(risk_analyst_approval='F')
        if has_context_params:
            redirect(URL('department', vars=dict(keywords=context_params)))
        else:
            redirect(URL('department'))

    if request.args(1) == 'process_type':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.process_type.id==request.args(0)).update(risk_manager_log=signature)
                db(db.process_type.id==request.args(0)).update(risk_manager_approval='T')
            elif request.args(2)=='0':
                db(db.process_type.id==request.args(0)).update(risk_manager_log=signature)
                db(db.process_type.id==request.args(0)).update(risk_manager_approval='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.process_type.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.process_type.id==request.args(0)).update(risk_analyst_approval='T')
            elif request.args(2)=='0':
                db(db.process_type.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.process_type.id==request.args(0)).update(risk_analyst_approval='F')
        if has_context_params:
            redirect(URL('process_type', vars=dict(keywords=context_params)))
        else:
            redirect(URL('process_type'))

    if request.args(1) == 'system_type':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.system_type.id==request.args(0)).update(risk_manager_log=signature)
                db(db.system_type.id==request.args(0)).update(risk_manager_approval='T')
            elif request.args(2)=='0':
                db(db.system_type.id==request.args(0)).update(risk_manager_log=signature)
                db(db.system_type.id==request.args(0)).update(risk_manager_approval='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.system_type.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.system_type.id==request.args(0)).update(risk_analyst_approval='T')
            elif request.args(2)=='0':
                db(db.system_type.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.system_type.id==request.args(0)).update(risk_analyst_approval='F')
        if has_context_params:
            redirect(URL('system_type', vars=dict(keywords=context_params)))
        else:
            redirect(URL('system_type'))

    if request.args(1) == 'process':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.process.id==request.args(0)).update(risk_manager_log=signature)
                db(db.process.id==request.args(0)).update(risk_manager_approval='T')
            elif request.args(2)=='0':
                db(db.process.id==request.args(0)).update(risk_manager_log=signature)
                db(db.process.id==request.args(0)).update(risk_manager_approval='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.process.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.process.id==request.args(0)).update(risk_analyst_approval='T')
            elif request.args(2)=='0':
                db(db.process.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.process.id==request.args(0)).update(risk_analyst_approval='F')
        if has_context_params:
            redirect(URL('process', vars=dict(keywords=context_params)))
        else:
            redirect(URL('process'))

    if request.args(1) == 'maturity_level':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.maturity_level.id==request.args(0)).update(risk_manager_log=signature)
                db(db.maturity_level.id==request.args(0)).update(risk_manager_approval='T')
            elif request.args(2)=='0':
                db(db.maturity_level.id==request.args(0)).update(risk_manager_log=signature)
                db(db.maturity_level.id==request.args(0)).update(risk_manager_approval='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.maturity_level.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.maturity_level.id==request.args(0)).update(risk_analyst_approval='T')
            elif request.args(2)=='0':
                db(db.maturity_level.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.maturity_level.id==request.args(0)).update(risk_analyst_approval='F')
        if has_context_params:
            redirect(URL('maturity_level', vars=dict(keywords=context_params)))
        else:
            redirect(URL('maturity_level'))

    if request.args(1) == 'objective_type':
        if (auth.has_membership(role='riskManager') or auth.has_membership(role='admin')):
            if request.args(2)=='1':
                db(db.objective_type.id==request.args(0)).update(risk_manager_log=signature)
                db(db.objective_type.id==request.args(0)).update(risk_manager_approval='T')
            elif request.args(2)=='0':
                db(db.objective_type.id==request.args(0)).update(risk_manager_log=signature)
                db(db.objective_type.id==request.args(0)).update(risk_manager_approval='F')
        elif (auth.has_membership(role='riskAnalyst')):
            if request.args(2)=='1':
                db(db.objective_type.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.objective_type.id==request.args(0)).update(risk_analyst_approval='T')
            elif request.args(2)=='0':
                db(db.objective_type.id==request.args(0)).update(risk_analyst_log=signature)
                db(db.objective_type.id==request.args(0)).update(risk_analyst_approval='F')
        if has_context_params:
            redirect(URL('objective_type', vars=dict(keywords=context_params)))
        else:
            redirect(URL('objective_type'))
    '''
