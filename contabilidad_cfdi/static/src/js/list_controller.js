/** @odoo-module */

import { ListController } from "@web/views/list/list_controller";
import {patch} from "@web/core/utils/patch";
import core from "web.core";
import framework from 'web.framework';
const qweb = core.qweb;
var session = require("web.session");

export const GroupControlExpand = {

    _onExportDIOTXLS(event) {
    debugger;
		event.stopPropagation();
        var self = this;
        var res_ids = [];
        var i;
        if (this.model.root.records.length){
            for(i=0;i<this.model.root.records.length;i++)
            {
                res_ids[i]=this.model.root.records[i].resId;
            }
        }
		var token = 'dummy-because-api-expects-one'
        framework.blockUI();
        session.get_file({
            url: '/web/export/xls_txt_diot_download',
            data: {record_ids: JSON.stringify(res_ids),report_type:'xls',token: token},
            complete: framework.unblockUI,
        });

	},
	_onExportDIOTTXT(event) {
	debugger;
		event.stopPropagation();
        var self = this;
        var res_ids = [];
        var i;
        if (this.model.root.records.length){
            for(i=0;i<this.model.root.records.length;i++)
            {
                res_ids[i]=this.model.root.records[i].resId;
            }
        }
        var token = 'dummy-because-api-expects-one'
		framework.blockUI();

        session.get_file({
            url: '/web/export/xls_txt_diot_download',
            data: {record_ids: JSON.stringify(res_ids),report_type:'txt',token: token},
            complete: framework.unblockUI,
        });
	},
};
patch(
    ListController.prototype,
    "contabilidad_cfdi.ListController",
    GroupControlExpand
);

