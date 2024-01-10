odoo.define('grcbit_zt.DashboardZT', function (require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var framework = require('web.framework');
    var session = require('web.session');
    var Dialog = require('web.Dialog');
    var _t = core._t;
    var apps_client = null;

    var DashboardZT = AbstractAction.extend({
        init: function (parent, action) {
            this._super(parent, action);
            var options = action.params || {};
            this.params = options;  // NOTE forwarded to embedded client action
        },
        start: function () {
            var self = this;
            self.view_dashboard_zt();
        },
        view_dashboard_zt: function () {
            var self = this;
            var def = $.Deferred();

            if (this.params.main_dashboard) {
                var domain = [];
                //this.getSession()
                session.user_has_group('grcbit_zt.group_dashboard_manager_zt')
                    .then(function (is_manager) {
                        if (is_manager) {
                            domain = [["main_dashboard", "=", true]]
                        } /*else {
                            domain = [["main_dashboard", "=", true], "|", ["user_id", "=", session.uid], ["user_id", "=", false]]
                        }*/
                        self._rpc({
                            model: 'backend.dashboard.zt',
                            method: 'search_read',
                            domain: domain,
                            fields: ['url', 'height', 'width'],
                            lazy: false,
                        }).then(function (res) {
                            if (res.length > 0) {
                                _.each(res, function (info) {
                                    var css = {
                                        width: info.width.toString() + '%',
                                        height: info.height.toString() + 'px',
                                        allow: 'fullscreen',
                                        scrolling: 'no',
                                        overflow:'hidden',
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
                    var css = {width: width, height: height,scrolling:'no',overflow:'hidden',};
                    self.$ifr = $('<iframe>').attr('src', url);
                    self.$ifr.appendTo(self.$('.o_content')).css(css);
                    self.$ifr.appendTo();
                }
                else{
                    var url_zt = this.params.url
                    var width = this.params.width.toString() + '%'
                    var height = this.params.height.toString() + 'px'
                    var css = {width: width, height: height,scrolling:'no',overflow:'hidden',};
                    self.$ifr = $('<iframe>').attr('src', url_zt);
                    self.$ifr.appendTo(self.$('.o_content')).css(css);
                    self.$ifr.appendTo();
                }
            }
            def.resolve();
            return def;
        }
    });



    core.action_registry.add("view_dashboard_zt", DashboardZT);
    return DashboardZT;

});
