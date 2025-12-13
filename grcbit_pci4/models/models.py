# -*- coding: utf-8 -*-
from odoo import api, models, fields, _

class PCIPrincipalRequirement(models.Model):
    _name = 'pci.principal.requirement'

    name = fields.Char(string="Name")
    description = fields.Html(string="Description")
    pci_requirement_ids = fields.One2many('pci.requirement', 'pci_principal_requirement_id')
    active = fields.Boolean(default=True)

class PCIRequirement(models.Model):
    _name = 'pci.requirement'
    name = fields.Char(string="Name")
    description= fields.Html(string="Description")
    pci_principal_requirement_id = fields.Many2one('pci.principal.requirement', string="PCI Principal Requirement")
    pci_section_ids = fields.One2many('pci.section', 'pci_requirement_id', string="PCI Section")
    active = fields.Boolean(default=True)

class PCISection(models.Model):
    _name = 'pci.section'

    name = fields.Char(string="Name")
    description= fields.Html(string="Description")
    pci_requirement_id = fields.Many2one('pci.requirement', string="PCI Requirement")
    pci_approach_req_ids = fields.One2many('pci.approach.requirement', 'pci_section_id', string="PCI DSS Requirement")
    active = fields.Boolean(default=True)

class PCIApproachRequirement(models.Model):
    _name = 'pci.approach.requirement'

    name = fields.Text(string="PCI DSS Requirement")
    description= fields.Html(string="Description")
    pci_section_id = fields.Many2one('pci.section', string="Requirement Description")
    assessment_finding = fields.Selection([
        ('in_place','In Place'),
        ('not_applicable','Not Applicable'),
        ('not_tested','Not Tested'),
        ('not_in_place','Not in Place'),
    ], string="Assessment Finding")
    below_method = fields.Selection([
        ('compensating_control','Compensating Control'),
        ('customized_approach','Customized Approach'),
    ], string="Method")
    testing_procedure_ids = fields.One2many('testing.procedure', 'pci_approach_req_id', string="Testing Procedure")
    pci_principal_req_id = fields.Many2one('pci.principal.requirement', related="pci_section_id.pci_requirement_id.pci_principal_requirement_id", store=True)
    pci_requirement_id = fields.Many2one('pci.requirement', related="pci_section_id.pci_requirement_id", store=True)
    pci_approach = fields.Many2one('pci.approach.requirement')
    active = fields.Boolean(default=True)

class  TestingProcedure(models.Model):
    _name = 'testing.procedure'

    testing_procedure = fields.Html(string="Testing Procedure")
    assessor_response = fields.Html(string="Assessor Response")
    pci_approach_req_id = fields.Many2one('pci.approach.requirement', string="PCI DSS Requirement")
    control_design_ids = fields.Many2many('control.design', string="Control Design")
    active = fields.Boolean(default=True)
