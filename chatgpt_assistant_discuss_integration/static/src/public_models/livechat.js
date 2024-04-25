/** @odoo-module **/

import {registerPatch} from '@mail/model/model_core';


function lpad(str, size) {
    str = "" + str;
    return new Array(size - str.length + 1).join('0') + str;
}

function datetime_to_str(obj) {
    if (!obj) {
        return false;
    }
    return lpad(obj.getUTCFullYear(), 4) + "-" + lpad(obj.getUTCMonth() + 1, 2) + "-"
        + lpad(obj.getUTCDate(), 2) + " " + lpad(obj.getUTCHours(), 2) + ":"
        + lpad(obj.getUTCMinutes(), 2) + ":" + lpad(obj.getUTCSeconds(), 2);
}


registerPatch({
    name: 'LivechatButtonView',
    recordMethods: {
        async _sendMessage(message) {
            this._super(...arguments);
            this.addMessage({
                id: new Date(),
                body: message.content,
                date: datetime_to_str(new Date()),
                is_discussion: true,
                temporary_to_delete: true,
            });
            this.messaging.publicLivechatGlobal.chatWindow.renderMessages();
        },
    }
});


registerPatch({
    name: 'PublicLivechatGlobalNotificationHandler',
    recordMethods: {
        _handleNotification({payload, type}) {
            this._super(...arguments);
            if (type === 'mail.channel/new_message') {
                this.messaging.publicLivechatGlobal.update({
                    messages: this.messaging.publicLivechatGlobal.messages.filter(message => !message.data.temporary_to_delete),
                });
                this.messaging.publicLivechatGlobal.chatWindow.renderMessages();
            }
        },
    }
});
