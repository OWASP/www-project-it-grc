/** @odoo-module **/

import BoardView from 'board.BoardView';
import core from 'web.core';
import dataManager from 'web.data_manager';

var QWeb = core.qweb;

BoardView.prototype.config.Controller.include({
    custom_events: _.extend({}, BoardView.prototype.config.Controller.prototype.custom_events, {
        save_dashboard: 'saveBoard',
    }),

    /**
     * Actually save a dashboard
     * @override
     *
     * @returns {Promise}
     */
    saveBoard: function () {
        const templateFn = renderToString.app.getTemplate("board.arch");
        const bdom = templateFn(this.board, {});
        const root = document.createElement("rendertostring");
        blockDom.mount(bdom, root);
        const result = xmlSerializer.serializeToString(root);
        const arch = result.slice(result.indexOf("<", 1), result.indexOf("</rendertostring>"));

        this.rpc("/web/view/edit_custom", {
            custom_id: this.board.customViewId,
            arch,
        });
        this.env.bus.trigger("CLEAR-CACHES");

    },
});