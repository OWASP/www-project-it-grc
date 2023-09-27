odoo.define('custom_dashboard.dashboard_action', function (require){
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var CustomDashBoard = AbstractAction.extend({
       template: 'CustomDashBoard',
    
    })
    core.action_registry.add('custom_dashboard_tags', CustomDashBoard);
    return CustomDashBoard;
    })