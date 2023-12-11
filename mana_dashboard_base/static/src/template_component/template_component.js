/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _lt } from "@web/core/l10n/translation";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

import { Component, xml } from "@odoo/owl";

export class TemplateWidget extends Component {

    get isReadonly() {
        return true;
    }

    setup() {
        super.setup();
    }
}

// props:
TemplateWidget.props = {
    ...standardFieldProps,
    template:  {
        type: String,
        optional: true,
    }
};

// extractProps
TemplateWidget.extractProps = ({ attrs }) => {
    return {
        template: attrs.options.template,
    };
};

TemplateWidget.displayName = _lt("TemplateWidget");

TemplateWidget.template = xml`
<div>
    <t t-call="{{this.props.template}}" />
</div>`

registry.category("fields").add("template_widget", TemplateWidget);
