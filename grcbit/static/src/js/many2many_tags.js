odoo.define('many2many_tags_click_cr.many2many', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');
    var FieldMany2ManyTags = relational_fields.FieldMany2ManyTags;
    var registry = require('web.field_registry');

    var FieldMany2manyOpen = FieldMany2ManyTags.extend({
        _renderTags: function () {
            this._super(...arguments);
            if(this.mode == 'readonly'){
                this.$el.on('click', 'div.badge-pill', this.onOpenRecordTag.bind(this));
            }
        },
        onOpenRecordTag:function(ev){
            var data = $(ev.target).parent()
            var data_element = data[0].parentElement
            if(data_element && data_element.getAttribute('data-id') != undefined && data_element.getAttribute('data-id')){
                this.do_action({
                    res_id: parseInt(data_element.getAttribute('data-id')),
                    res_model: this.field.relation,
                    type: 'ir.actions.act_window',
                    views: [[false, 'form']],
                });
            }
        },
        _getRenderTagsContext: function () {
            var result = this._super.apply(this, arguments);
            result.res_model = this.field.relation;
            return result;
        },
    });
    registry
    .add('many2many_tags_open', FieldMany2manyOpen)
    return FieldMany2manyOpen

    
});