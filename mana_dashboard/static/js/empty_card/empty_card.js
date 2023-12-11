/**
 * empty card
 */
odoo.define('mana_dashboard.empty_card', function (require) {
    "use strict";

    const BlockRegistry = require('mana_dashboard.block_registry');
    const QwebBlock = require('mana_dashboard.qweb_block');

    const QWebBlockModel = QwebBlock.QWebBlockModel;
    const QWebBlockView = QwebBlock.QWebBlockView;

    const icons = require('mana_dashboard.icons');
    const core = require('web.core');

    let _t = core._t;

    function builder(editor, options) {

        const dc = editor.DomComponents;

        /**
         * empty card
         */
        editor.BlockManager.add('empty_card', {
            label: _t('Empty Card'),
            category: _t('Basic'),
            select: true,

            render: () => {
                return `<div class="d-flex flex-column align-items-center justify-content-center"><div class="chart-icon">${icons.card_svg}</div><div class='anita-block-label'>Empty Card</div></div>`
            },

            content: {
                type: 'empty_card'
            }
        });

        /**
         * empty card
         */
        dc.addType('empty_card', {

            model: QWebBlockModel.extend({
                defaults: {
                    ...QWebBlockModel.prototype.defaults,

                    name: _t('Empty Card'),
                    classes: ['card'],

                    default_template: 'mana_dashboard.empty_card_style_one',
                    template_category: 'empty_card',
                    template_type: 'empty_card',
                    search_sensitive: false,
                    auto_load_config: true,
                    dynamic_default_template: true,

                    fetch_data: false,
                    has_script: false,
                    toolbar_config: {
                        edit_config: false,
                    },

                    traits: [
                        {
                            type: 'form_trait',
                            name: 'form_trait',
                            label: 'Form',
                            model: 'mana_dashboard.config',
                            form_view_ref: 'mana_dashboard.simple_config_form',
                            changeProp: 1,
                        }
                    ]
                },

                initialize() {
                    QWebBlockModel.prototype.initialize.apply(this, arguments);
                    this.listenTo(this, 'change:form_trait', this.on_form_trait_change);
                    this.init_config();
                },

                init_config: function () {

                    let config_id = this.get('attributes').config_id;
                    if (config_id) {
                        return;
                    }
        
                    if (!this.get('has_config')) {
                        return;
                    }

                    let widget = this.get_widget();
                    let dashboard_id = this.get_widget().dashboard_id;
                    let config_model = this.get('config_model');
                    let component_type = this.get('type');
                    let default_template = widget.get_default_template(
                        component_type) || this.get('default_template');

                    return this._rpc({
                        "model": 'mana_dashboard.any_config',
                        "method": "create_config",
                        "args": [dashboard_id, config_model, {
                            'default_template': default_template,
                            'template_category': this.get('template_category'),
                            'template_type': this.get('template_type')
                        }],
                    }, {
                        "shadow": true,
                    }).then((result) => {
                        this.addAttributes({ 'config_id': result.config_id });
                    });
                },

                on_form_trait_change() {
                    this.reload_config();
                },
            }, {
                isComponent: (el) => {
                    if (el && el.classList && el.classList.contains('empty_card')) {
                        return {
                            type: 'empty_card',
                        };
                    }
                }
            }),

            view: QWebBlockView.extend({
                events: {},

                init() {
                    QWebBlockView.prototype.init.apply(this, arguments);
                },

                render(...args) {
                    QWebBlockView.prototype.render.apply(this, args);
                    return this;
                }
            })
        });
    }

    BlockRegistry.add('empty_card', builder);

    return builder
});
