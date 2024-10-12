# -*- coding: utf-8 -*-
from odoo import api, models, fields, _

class PCIPrincipalRequirement(models.Model):
    _name = 'pci.principal.requirement'

    name = fields.Char(string="Name")
    description = fields.Html(string="Description")

class PCIRequirement(models.Model):
    _name = 'pci.requirement'
    name = fields.Char(string="Name")
    description= fields.Html(string="Description")
    pci_principal_requirement_id = fields.Many2one('pci.principal.requirement', string="PCI Principal Requirement")

class PCISection(models.Model):
    _name = 'pci.section'

    name = fields.Char(string="Name")
    description= fields.Html(string="Description")
    pci_requirement_id = fields.Many2one('pci.requirement', string="PCI Requirement")

class PCIApproachRequirement(models.Model):
    _name = 'pci.approach.requirement'

    name = fields.Char(string="Name")
    description= fields.Html(string="Description")
    pci_section_id = fields.Many2one('pci.section', string="PCI Section")
    assessment_finding = fields.Selection([
        ('in_place','In Place'),
        ('not_applicable','Not Applicable'),
        ('not_tested','Not Tested'),
        ('not_in_place','Not in Place'),
    ], strig="Assessment Finding")

    below_method = fields.Selection([
        ('compensating_control','Compensating Control'),
        ('customized_approach','Customized Approach'),
    ], strig="Below Method")

    testing_procedure = fields.Char(string="Testing Procedure")
    assessor_response = fields.Char(string="Assessor Response")