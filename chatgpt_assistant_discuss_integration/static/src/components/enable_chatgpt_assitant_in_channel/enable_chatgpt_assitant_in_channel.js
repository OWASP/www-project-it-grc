/** @odoo-module */

import {registry} from "@web/core/registry"
import {listView} from "@web/views/list/list_view"
import {ListController} from "@web/views/list/list_controller"
import {useService} from "@web/core/utils/hooks"


import {ThreadViewTopbar} from '@mail/components/thread_view_topbar/thread_view_topbar';
import {registerMessagingComponent} from '@mail/utils/messaging_component';

const {Component, useState, onWillStart, useRef} = owl;

class ThreadViewTopbarComponent extends ThreadViewTopbar {
    setup() {
        super.setup()
        this.action = useService("action")
        this.model = "mail.channel"
    }

    async openChannelForChatGPT() {
        const channel_id = this.props.record.thread.channel?.id
        await this.action.doAction({
            "type": "ir.actions.act_window",
            "res_model": "mail.channel",
            "views": [[false, "form"]],
            "res_id": channel_id,
        });
    }
}

Object.assign(ThreadViewTopbarComponent, {
    props: {record: Object},
    template: 'chatgpt_assistant_discuss_integration.ThreadViewTopbarComponent',
});

registerMessagingComponent(ThreadViewTopbarComponent);
