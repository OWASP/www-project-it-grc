# Copyright 2019 Stefano Consolaro (Ass. PNLUG - Gruppo Odoo <http://odoo.pnlug.it>)

from odoo import _, api, fields, models


class MgmtsystemNonconformity(models.Model):
    """
    Extend nonconformity adding fields for type,
    quantity checked and quantity non compliant,
    adding method to send email
    """

    _inherit = ["mgmtsystem.nonconformity"]

    # new fields
    # nonconformity type
    nc_type = fields.Selection(
        [
            ("internal", "Internal"),
            ("supplier", "Supplier"),
            ("customer", "Customer"),
            ("external", "External"),
        ],
        "Type",
        default="internal",
    )
    # quantity checked to reveal the nonconformity [qty-ck]
    qty_checked = fields.Float("Quantity checked")
    # quantity found to be non-compliant with the inspection [qty-nc]
    qty_noncompliant = fields.Float("Quantity non-compliant")
    # utility name of quality contact
    quality_contact_name = fields.Char("Contact Name")
    # utility e-mail of quality contact
    quality_contact_email = fields.Char("Email")

    # define constraints for quantities

    @api.onchange("qty_noncompliant")
    def _onchange_qty_noncompliant(self):
        """
        set qty checked equal to qty non compliant if it is lower
        (qty-ck can not be lower to qty-nc)
        """
        if self.qty_noncompliant > self.qty_checked:
            self.qty_checked = self.qty_noncompliant

    @api.onchange("qty_checked")
    def _onchange_qty_checked(self):
        """
        set qty non compliant equal to qty checked if it is higher
        qty-nc can not be greater to qty-ck
        """
        if self.qty_checked < self.qty_noncompliant:
            self.qty_noncompliant = self.qty_checked

    # new method
    def action_nc_sent(self, test_module=False):
        """
        send document to partner email
        if address not exists raises an error message
        todo: use a better way to test module availability
        """
        if (
            "quality" not in self.env["res.partner"]._fields["type"].get_values([])
            or test_module
        ):
            # raise an error for module not installed
            message = _(
                "The partner's contacts quality type isn't available.\n "
                "Check if module mgmtsystem_nonconformity_partner is installed."
            )
            raise models.ValidationError(message)

        # get first contact of type quality
        contact_quality = self.partner_id["child_ids"].search(
            [("parent_id", "=", self.partner_id.id), ("type", "=", "quality")], limit=1
        )

        if contact_quality["email"]:
            self.quality_contact_name = contact_quality["name"]
            self.quality_contact_email = contact_quality["email"]
            # find the e-mail template
            report_tmplt = self.env.ref(
                "mgmtsystem_nonconformity_type.email_template_nonconformity"
            )

            # send out the e-mail template to the partner
            self.env["mail.template"].browse(report_tmplt.id).send_mail(self.id)

        else:
            # raise an error for field not compiled
            raise models.ValidationError(
                _(
                    "The partner's quality contact email "
                    "is required in order to send the message."
                )
            )

        return True
