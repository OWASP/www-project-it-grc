# -*- coding: utf-8 -*-

import inspect

from odoo import models, _
from odoo.exceptions import AccessError
from odoo.models import check_method_name


class AnitaViewExtend(models.Model):
    '''
    anita view extend
    '''
    _inherit = 'ir.ui.view'

    def _validate_tag_button(self, node, name_manager, node_info):
        if not node_info['validate']:
            return
        name = node.get('name')
        special = node.get('special')
        type_ = node.get('type')
        if special:
            if special not in ('cancel', 'save', 'add', 'save_and_return', 'save_and_notify', 'just_notify'):
                self._raise_view_error(_("Invalid special '%(value)s' in button", value=special), node)
        elif type_:
            if type_ == 'edit': # list_renderer, used in kanban view
                return
            elif not name:
                self._raise_view_error(_("Button must have a name"), node)
            elif type_ == 'object':
                func = getattr(type(name_manager.model), name, None)
                if not func:
                    msg = _(
                        "%(action_name)s is not a valid action on %(model_name)s",
                        action_name=name, model_name=name_manager.model._name,
                    )
                    self._raise_view_error(msg, node)
                try:
                    check_method_name(name)
                except AccessError:
                    msg = _(
                        "%(method)s on %(model)s is private and cannot be called from a button",
                        method=name, model=name_manager.model._name,
                    )
                    self._raise_view_error(msg, node)
                try:
                    inspect.signature(func).bind(self=name_manager.model)
                except TypeError:
                    msg = "%s on %s has parameters and cannot be called from a button"
                    self._log_view_warning(msg % (name, name_manager.model._name), node)
            elif type_ == 'action':
                # logic mimics /web/action/load behaviour
                action = False
                try:
                    action_id = int(name)
                except ValueError:
                    model, action_id = self.env['ir.model.data']._xmlid_to_res_model_res_id(name, raise_if_not_found=False)
                    if not action_id:
                        msg = _("Invalid xmlid %(xmlid)s for button of type action.", xmlid=name)
                        self._raise_view_error(msg, node)
                    if not issubclass(self.pool[model], self.pool['ir.actions.actions']):
                        msg = _(
                            "%(xmlid)s is of type %(xmlid_model)s, expected a subclass of ir.actions.actions",
                            xmlid=name, xmlid_model=model,
                        )
                        self._raise_view_error(msg, node)
                action = self.env['ir.actions.actions'].browse(action_id).exists()
                if not action:
                    msg = _(
                        "Action %(action_reference)s (id: %(action_id)s) does not exist for button of type action.",
                        action_reference=name, action_id=action_id,
                    )
                    self._raise_view_error(msg, node)

            name_manager.has_action(name)

        if node.get('icon'):
            description = 'A button with icon attribute (%s)' % node.get('icon')
            self._validate_fa_class_accessibility(node, description)
