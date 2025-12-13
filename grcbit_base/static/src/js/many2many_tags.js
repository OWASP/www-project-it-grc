/** @odoo-module **/
// author: Candidroot Solutions Pvt Ltd
import { registry } from "@web/core/registry";
import { Many2ManyTagsField } from "@web/views/fields/many2many_tags/many2many_tags_field";
const { onWillUpdateProps } = owl;
    export class TagsOpenMany2ManyTagsField extends Many2ManyTagsField {
        getTagProps(record) {
            const props = super.getTagProps(record);
            props.onClick = (ev) => this.onOpenClick(ev, record);
            return props;
        }
        onOpenClick(ev, record) {
            if(record.resModel && record.data.id){
                this.env.model.actionService.doAction({
                    type: "ir.actions.act_window",
                    res_model: record.resModel,
                    res_id: record.data.id,
                    views: [[false, "form"]],
                    view_mode: "form",
                });
            }
        }
    }
registry.category("fields").add("many2many_tags_open", TagsOpenMany2ManyTagsField);
