odoo.define('powerbi_dashboard.DashboardRewrite', function (require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var Widget = require('web.Widget');
var core = require('web.core');
var web_client = require('web.web_client');
var _t = core._t;
var QWeb = core.qweb;

//var HrDashboard1 = Widget.extend({
var HrDashboard1 = AbstractAction.extend({
    template: 'HrDashboardMain1',
    init: function(parent, context) {
        this._super(parent, context);
    },

    willStart: function(){
        var self = this;
            return this._super()
        .then(function() {
        return self;
        });
    },

    start: function() {
        console.log("START FUNCTION")
        var self = this;
        this.set("title", 'Dashboard');
        return this._super().then(function() {
            self.update_cp();
            self.render_dashboards();
            self.$el.parent().addClass('oe_background_grey');
        });
    },

    render_dashboards: function() {
        var self = this;
        self.$('.o_hr_dashboard').append(QWeb.render('iframe12', {widget: self}));

    },

    update_cp: function() {
        var self = this;
    },

   });

    core.action_registry.add('powerbi_dashboard', HrDashboard1);

return HrDashboard1;

});