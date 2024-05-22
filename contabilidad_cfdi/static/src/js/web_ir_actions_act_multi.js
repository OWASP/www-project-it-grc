odoo.define('contabilidad_cfdi.ir_actions_act_multi_print', function (require) {
"use strict";

    var ActionManager = require('web.ActionManager');
    
    ActionManager.include({
    	_handleAction: function (action, options) {
            if (action.type === 'ir.actions.act_multi_print') {
                return this._executeMultiAction(action, options);
            }
            return this._super.apply(this, arguments);
        },
        _executeMultiAction: function(action, options){
            var self = this;

            var i = 0;
            var res;
            for(i=0;i<action.actions.length;i++)
            	{
            	if (action.actions[i].type=='ir.actions.act_url'){
            		res = self._executeURLAction(action.actions[i],options);
            	}
            	else if(action.actions[i].type=='ir.actions.act_window'){
            		res = self._executeWindowAction(action.actions[i],options)
            	}
            	
            	}
            return res;
        },

    });
    
});
