# -*- coding: utf-8 -*-
from odoo import api, models, fields, _

class PCIPrincipalRequirement(models.Model):
    _name = 'pci.principal.requirement'

    name = fields.Char(string="Name")
    description = fields.Html(string="Description")

    pci_requirement_ids = fields.One2many('pci.requirement', 'pci_principal_requirement_id')

class PCIRequirement(models.Model):
    _name = 'pci.requirement'
    name = fields.Char(string="Name")
    description= fields.Html(string="Description")
    pci_principal_requirement_id = fields.Many2one('pci.principal.requirement', string="PCI Principal Requirement")
    pci_section_ids = fields.One2many('pci.section', 'pci_requirement_id', string="PCI Section")

class PCISection(models.Model):
    _name = 'pci.section'

    name = fields.Char(string="Name")
    description= fields.Html(string="Description")
    pci_requirement_id = fields.Many2one('pci.requirement', string="PCI Requirement")

    pci_approach_req_ids = fields.One2many('pci.approach.requirement', 'pci_section_id', string="PCI Approach rRequirement")

class PCIApproachRequirement(models.Model):
    _name = 'pci.approach.requirement'

    name = fields.Html(string="PCI DSS Requirement")
    description= fields.Html(string="Description")
    pci_section_id = fields.Many2one('pci.section', string="Requirement Description")
    assessment_finding = fields.Selection([
        ('in_place','In Place'),
        ('not_applicable','Not Applicable'),
        ('not_tested','Not Tested'),
        ('not_in_place','Not in Place'),
    ], strig="Assessment Finding")

    below_method = fields.Selection([
        ('compensating_control','Compensating Control'),
        ('customized_approach','Customized Approach'),
    ], strig="Method")
    testing_procedure_ids = fields.One2many('testing.procedure', 'pci_approach_req_id', string="Testing Procedure")


class  TestingProcedure(models.Model):
    _name = 'testing.procedure'

    testing_procedure = fields.Html(string="Testing Procedure")
    assessor_response = fields.Html(string="Assessor Response")
    pci_approach_req_id = fields.Many2one('pci.approach.requirement', string="Approach requirement")