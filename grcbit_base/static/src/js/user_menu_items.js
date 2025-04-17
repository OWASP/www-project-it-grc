/** @odoo-module **/

import { registry } from "@web/core/registry";
import { preferencesItem } from "@web/webclient/user_menu/user_menu_items";
import { documentationItem } from "@web/webclient/user_menu/user_menu_items";

export function hidePreferencesItem(env)  {
    return Object.assign(
        {},
        preferencesItem(env),
        {
            type: "",
            id: "",
            description: env._t(""),
            callback: async function () {},
            sequence: 0,
        }
    );
}

registry.category("user_menuitems").add('support', hidePreferencesItem, { force: true }).add("documentation", hidePreferencesItem, { force: true }).add("odoo_account", hidePreferencesItem, { force: true }).add("shortcuts", hidePreferencesItem, { force: true })