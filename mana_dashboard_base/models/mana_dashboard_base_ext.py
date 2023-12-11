# -*- coding: utf-8 -*-

from odoo import models, api, exceptions, fields, _, tools
from odoo.fields import Field
import logging

_logger = logging.getLogger(__name__)


class EnigmaBaseExtend(models.AbstractModel):
    """
    base extend
    """
    _inherit = "base"

    @api.model
    def _add_inherited_fields(self):
        """
        extend to add custom code
        """
        super(EnigmaBaseExtend, self)._add_inherited_fields()
        self._after_inherited_fields()

    @api.model
    def _add_field_ext(self, name, field):
        """ Add the given ``field`` under the given ``name`` in the class """
        # cls = type(self)
        # # add field as an attribute and in cls._fields (for reflection)
        # if not isinstance(getattr(cls, name, field), Field):
        #     _logger.warning("In model %r, field %r overriding existing value", cls._name, name)
        # setattr(cls, name, field)
        # field._toplevel = True
        # field.__set_name__(cls, name)
        # field._module = cls._module
        # cls._fields[name] = field
        # cls._field_definitions.append(field)
        self._add_field(name, field)

    @api.model
    def _after_inherited_fields(self):
        pass
