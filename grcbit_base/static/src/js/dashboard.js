odoo.define('custom_dashboard.dashboard_action', function (require){
   "use strict";
   var AbstractAction = require('web.AbstractAction');
   var core = require('web.core');
   var QWeb = core.qweb;
   var rpc = require('web.rpc');
   var ajax = require('web.ajax');
   var CustomDashBoard = AbstractAction.extend({
      template: 'CustomDashBoard',
      init: function(parent, context) {
         this._super(parent, context);
         this.dashboard_templates = ['DashboardProject'];
      },
      
      start: function() {
         var self = this;
         this.set("title", 'Dashboard');
         return this._super().then(function() {
             self.render_dashboards();
         });
         
     },
     willStart: function(){
         var self = this;
         return this._super()
     },
      render_dashboards: function() {
         var self = this;
         var chart = new Chart('new_custom_chart', {
            type: 'pie',
            data: {
               datasets: [{
                   backgroundColor: "purple",
                   data: [0, 10, 20, 30, 40]
               }]
           },
            options: {}
         });
         // this.fetch_data()
         var templates = []
         var templates = ['DashboardProject'];
         _.each(templates, function(template) {
            self.$('.o_hr_dashboard').append(QWeb.render(template, {widget: self}))
         });
         
      },
      // fetch_data: function() {
      //    var self = this
      //    var def1 = this._rpc({
      //        model: 'data.inventory',
      //        method: "get_data",
      //    })
      //    .then(function (result) {
      //        $('#it_system').append('<span>' + result.it_system + '</span>');
      //        $('#third_party').append('<span>' + result.third_party + '</span>');
      //       //  $('#products_storable').append('<span>' + result.storable + '</span>');
      //       //  $('#product_consumable').append('<span>' + result.consumable + '</span>');
      //    });
      // },
   });
   core.action_registry.add('custom_dashboard_tags', CustomDashBoard);
   return CustomDashBoard;

})