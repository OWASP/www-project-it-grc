odoo.define('nomina_cfdi.CajaNomina', function (require) {
"use strict";

var ListController = require('web.ListController');
var core = require('web.core');
var _t = core._t;

ListController.include({
	renderButtons: function ($node) {
		this._super($node)
	  	debugger;
	  	if (this.modelName==='caja.nomina'){
             var $import_button = $("<button type='button' class='btn btn-primary btn-sm o_list_entrega_fondo o_radio_hide_bullet label' accesskey='entrega_fondo'>Entrega Fondo / Caja</button>");
             $import_button.attr('style', 'padding-top: 5px;padding-bottom: 4px;padding-right: 9px;padding-left: 9px;margin-left: 6px;');
             this.$buttons.find(".o_list_button_add").after($import_button);
             this.$buttons.on('click', '.o_list_entrega_fondo', this._onEntregaFondo.bind(this));
         }
    	},
    
     _onEntregaFondo: function (event) {
    	var self = this;
   		console.log('okok')
   		this.do_action({
            type: "ir.actions.act_window",
            name: "Altas y Bajas",
            res_model: "entrega.fondo.caja",
            views: [[false,'form']],
            target: 'new',
            view_type : 'form',
            view_mode : 'form',
        });
    },
	
});

});
