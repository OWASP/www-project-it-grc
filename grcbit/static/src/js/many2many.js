odoo.define('grcbit.many2many', function (require) {
"use strict";

var core = require('web.core');
var dialogs = require('web.view_dialogs');
var registry = require('web.field_registry');
var rel_fields = require('web.relational_fields');
var _t = core._t;

var FieldMany2ManyTagLinks = rel_fields.FieldMany2ManyTags.extend({
get_badge_id: function (el) {
if ($(el).hasClass('badge')) return $(el).data('id');
return $(el).closest('.badge').data('id');
},
events: _.extend({}, rel_fields.FieldMany2ManyTags.prototype.events, {
'click .badge': function (e) {
e.stopPropagation();
var self = this;
var record_id = this.get_badge_id(e.target);
new dialogs.FormViewDialog(self, {
res_model: self.field.relation,
res_id: record_id,
context: self.record.getContext(),
title: _t('Open: ') + self.field.string,
readonly: !self.attrs.can_write,
}).on('write_completed', self, function () {
self.dataset.cache[record_id].from_read = {};
self.dataset.evict_record(record_id);
self.render_value();
}).open();
}
})
});
registry.add('many2many_taglinks', FieldMany2ManyTagLinks);

return {
FieldMany2ManyTagLinks: FieldMany2ManyTagLinks
};

});
