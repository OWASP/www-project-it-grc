# -*- coding: utf-8 -*-

from odoo.tools.safe_eval import datetime, time, wrap_module
from odoo import exceptions, _
import pendulum

def get_eval_context(self):
    """
    eval context
    """
    context = {
        # orm
        'env': self.env,
        'self': self,
        # Exceptions
        'Warning': exceptions.Warning,
        'UserError': exceptions.UserError,
        'datetime': datetime,
        'context_today': datetime.datetime.now,
        'user': self.env.user.with_context({}),
        'time': time,
        'res_company': self.env.company.sudo(),
        'json5': wrap_module(__import__('json5'), ['loads', 'dumps']),
        # import math functions
        'math': wrap_module(__import__('math'), ['sqrt', 'log', 'log10', 'log2', 'exp', 'cos', 'sin', 'tan', 
            'acos', 'asin', 'atan', 'atan2', 'cosh', 'sinh', 'tanh', 'acosh', 'asinh', 'atanh', 'ceil'])
    }
    return context
