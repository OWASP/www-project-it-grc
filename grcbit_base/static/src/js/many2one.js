odoo.define('grcbit.many2one', function (require) {
"use strict";

    var relational_fields = require('web.relational_fields');
    var core = require('web.core');

    var _t = core._t;
    var _lt = core._lt;
    var qweb = core.qweb;


    relational_fields.FieldMany2One.include({
        _renderReadonly: function () {
            var escapedValue = _.escape((this.m2o_value || "").trim());
            var value = escapedValue.split('\n').map(function (line) {
                return '<span>' + line + '</span>';
            }).join('<br/>');
            this.$el.html(value);
            if (!this.noOpen && this.value) {
                var queryString = window.location.hash.substring(1);
                var urlParams = new URLSearchParams(queryString);
                var menuId = urlParams.get('menu_id') || '';

                this.$el.attr('href', _.str.sprintf('#id=%s&model=%s&menu_id=%s', this.value.res_id, this.field.relation, menuId));
                this.$el.addClass('o_form_uri');
            }
        },

        _renderEdit: function () {
            this._super.apply(this, arguments);

            if (!this.noOpen && this.value) {
                var queryString = window.location.hash.substring(1);
                var urlParams = new URLSearchParams(queryString);
                var menuId = urlParams.get('menu_id') || '';

                this.$el.find('.o_external_button').attr('href', _.str.sprintf('#id=%s&model=%s&menu_id=%s', this.value.res_id, this.field.relation, menuId));
                
            }
        },

        _onExternalButtonClick: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();

            this._super.apply(this, arguments);
        }
    });

});


