odoo.define('backend_iframe.Dashboard', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var framework = require('web.framework');
    var session = require('web.session');
    var Dialog = require('web.Dialog');
    var _t = core._t;
    var apps_client = null;

    var Dashboard = AbstractAction.extend({
        init: function (parent, action) {
            this._super(parent, action);
            var options = action.params || {};
            this.params = options;  // NOTE forwarded to embedded client action
        },
        start: function () {
            var self = this;
            self.view_dashboard();
        },
        view_dashboard: function () {
            var self = this;
            var def = $.Deferred();

            if (this.params.main_dashboard) {
                var domain = [];
                //this.getSession()
                session.user_has_group('backend_iframe.group_dashboard_manager')
                    .then(function (is_manager) {
                        if (is_manager) {
                            domain = [["main_dashboard", "=", true]]
                        } /*else {
                            domain = [["main_dashboard", "=", true], "|", ["user_id", "=", session.uid], ["user_id", "=", false]]
                        }*/
                        self._rpc({
                            model: 'backend.dashboard',
                            method: 'search_read',
                            domain: domain,
                            fields: ['url', 'height', 'width','url_zt','zerotrust_enable'],
                            lazy: false,
                        }).then(function (res) {
                            if (res.length > 0) {
                                _.each(res, function (info) {
                                    var css = {
                                        width: info.width.toString() + '%',
                                        height: info.height.toString() + 'px',
                                        allow: 'fullscreen'
                                    };
                                    if(res[0].zerotrust_enable == false){
                                        var $ifr = $('<iframe>').attr('src', info.url);
                                    }
                                    else{
                                        var $ifr = $('<iframe>').attr('src', info.url_zt);
                                    }
                                    $ifr.appendTo(self.$('.o_content')).css(css);
                                    self.$ifr += $ifr
                                })
                            } /*else {
                                Dialog.alert(this, _t("You don't have any Main Dashboard, Please Select at least one main Dashboard !"), {
                                    title: _t('Warning'),
                                });
                                return;
                            }*/
                        })
                    })
            } else {
                if(this.params.zerotrust_enable == false){
                    var url = this.params.url
                    var width = this.params.width.toString() + '%'
                    var height = this.params.height.toString() + 'px'
                    var css = {width: width, height: height};
                    self.$ifr = $('<iframe>').attr('src', url);
                    self.$ifr.appendTo(self.$('.o_content')).css(css);
                    self.$ifr.appendTo();
                }
                else{
                    var url_zt = this.params.url_zt
                    var width = this.params.width.toString() + '%'
                    var height = this.params.height.toString() + 'px'
                    var css = {width: width, height: height};
                    self.$ifr = $('<iframe>').attr('src', url_zt);
                    self.$ifr.appendTo(self.$('.o_content')).css(css);
                    self.$ifr.appendTo();
                }
            }
            def.resolve();
            return def;
        }
    });



    core.action_registry.add("view_dashboard", Dashboard);
    return Dashboard;

});
