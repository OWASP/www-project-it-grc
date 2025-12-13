from odoo import models
from odoo.exceptions import ValidationError

class ResUsersInh(models.Model):
    _inherit = 'res.users'

    def write(self, vals):
        for rec in self:
            current_user = rec.env['res.users'].sudo().browse(
                rec._context.get('uid', rec.env.user.id)
            )

            try:
                admin_user = rec.env.ref('base.user_admin', raise_if_not_found=False)
            except Exception:
                admin_user = None

            if not admin_user or self.env.context.get('install_mode'):
                return super().write(vals)

            if rec.id == admin_user.id and current_user.id != admin_user.id:
                raise ValidationError("You cannot modify the administrator user (base.user_admin).")

            if current_user.id == rec.id:
                continue

            has_grc_group = False
            try:
                has_grc_group = current_user.has_group('grcbit_base.group_grc_admin')
            except Exception:
                pass

            if not has_grc_group:
                raise ValidationError("You do not have permission to modify this user.")

        return super().write(vals)

    def unlink(self):
        admin_user = self.env.ref('base.user_admin', raise_if_not_found=False)
        if admin_user and admin_user in self and not self.env.context.get('install_mode'):
            raise ValidationError("You cannot delete the administrator user (base.user_admin).")
        return super().unlink()

    def copy(self, default=None):
        admin_user = self.env.ref('base.user_admin', raise_if_not_found=False)
        if admin_user and self.id == admin_user.id and not self.env.context.get('install_mode'):
            raise ValidationError("You cannot duplicate the administrator user (base.user_admin).")
        return super().copy(default)

