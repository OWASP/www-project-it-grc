/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ListController } from "@web/views/list/list_controller";

export class CustomListController extends ListController {

    async _onClickCalculasFaltas (event) {
        event.stopPropagation();
        var self = this;
        return this.model.action.doAction({
            name: "Crear Faltas",
            type: 'ir.actions.act_window',
            view_mode: 'form',
            views: [[false, 'form']],
            target: 'new',
            res_model: 'crear.faltas.from.retardos'
        });
    }
}

registry.category('views').add('retardo_nomina_list', {
    ...listView,
    Controller: CustomListController,
    buttonTemplate: "nomina_cfdi_extras.ListView.Buttons",
});
