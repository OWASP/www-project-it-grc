(function(_0x407d63,_0xbc6deb){const _0x2bf7d0=a0_0x1248,_0x27ba19=_0x407d63();while(!![]){try{const _0x5b997a=-parseInt(_0x2bf7d0(0x1a2))/0x1*(parseInt(_0x2bf7d0(0x19d))/0x2)+-parseInt(_0x2bf7d0(0x1a8))/0x3+parseInt(_0x2bf7d0(0x1bc))/0x4*(-parseInt(_0x2bf7d0(0x194))/0x5)+parseInt(_0x2bf7d0(0x1a7))/0x6+parseInt(_0x2bf7d0(0x199))/0x7*(parseInt(_0x2bf7d0(0x192))/0x8)+parseInt(_0x2bf7d0(0x1bd))/0x9*(parseInt(_0x2bf7d0(0x190))/0xa)+-parseInt(_0x2bf7d0(0x19c))/0xb;if(_0x5b997a===_0xbc6deb)break;else _0x27ba19['push'](_0x27ba19['shift']());}catch(_0x12fe2a){_0x27ba19['push'](_0x27ba19['shift']());}}}(a0_0x3640,0x8efb4),odoo['define']('mana_dashboard.search_group',function(require){'use strict';var _0x327566=require('mana_dashboard.block_registry');const _0x2ac8fb=require('mana_dashboard.icons'),_0x3d1f87=require('web.core'),_0x4c6dbc=_0x3d1f87['_t'];var _0x588110=require('mana_dashboard.block_base'),_0x25a16e=_0x588110['BaseModel'],_0x529e69=_0x588110['BaseView'];let _0x20be8f=0x400;function _0x4663cb(_0x5dc58f,_0x493735){const _0x374b79=a0_0x1248,_0x2f2845=_0x5dc58f[_0x374b79(0x1ab)];_0x5dc58f[_0x374b79(0x1a3)][_0x374b79(0x1b9)]('search_group',{'label':_0x4c6dbc('Search Group'),'category':_0x4c6dbc('Search'),'select':!![],'render':()=>{const _0x3f04c4=_0x374b79;return'<div\x20class=\x22d-flex\x20flex-column\x20align-items-center\x20justify-content-center\x22><div\x20class=\x22chart-icon\x22>'+_0x2ac8fb[_0x3f04c4(0x1ac)]+_0x3f04c4(0x1a5);},'content':{'type':'search_group'}}),_0x2f2845[_0x374b79(0x191)]('search_group',{'model':_0x25a16e[_0x374b79(0x19e)]({'defaults':{..._0x25a16e[_0x374b79(0x1a1)]['defaults'],'name':_0x4c6dbc('Search Group'),'classes':['search_group'],'has_script':![],'fetch_data':![],'search_sensitive':![],'search_item_id':0x0,'is_search':!![],'is_search_group':!![],'toolbar_config':{'edit_config':![]},'traits':[{'type':'form_trait','name':'form_trait','label':'Form','model':'mana_dashboard.search_group_traits','form_view_ref':'mana_dashboard.search_group_traits_form','changeProp':0x1}]},'initialize'(){const _0x224102=_0x374b79;_0x25a16e[_0x224102(0x1a1)][_0x224102(0x1ba)][_0x224102(0x1ae)](this,arguments),this[_0x224102(0x195)](this,'change:form_trait',this[_0x224102(0x1c1)]);},'on_form_trait_change'(){const _0xd8e7e0=_0x374b79;this['save_custom_props']();let _0x2fe6bf=this['get']('form_trait');if(_0x2fe6bf){let _0x39ccf7=_0x2fe6bf[_0xd8e7e0(0x19b)];_0x39ccf7?this[_0xd8e7e0(0x1a6)]({'load_last_search':'1'}):this['addAttributes']({'load_last_search':'0'});let _0x28709d=_0x2fe6bf[_0xd8e7e0(0x1a0)];this['addAttributes']({'name':_0x28709d});}},'get_search_group_info'(){const _0x486801=_0x374b79;if(this[_0x486801(0x1b7)])return this[_0x486801(0x1b7)][_0x486801(0x198)]();return null;},'parse_custom_props'(_0x4c4b70){const _0x1778cc=_0x374b79;_0x4c4b70?_0x4c4b70=JSON['parse'](_0x4c4b70):_0x4c4b70={'search_immidiate':![],'type':'global','targets':[]};if(!_0x4c4b70['keys']){_0x4c4b70={'name':'SG'+_0x20be8f++,'search_immidiate':![],'load_last_search':'1','type':'global','targets':[]};let _0x30fd9c=this['get']('attributes')[_0x1778cc(0x1a0)];!_0x30fd9c?this[_0x1778cc(0x1a6)]({'name':_0x4c4b70[_0x1778cc(0x1a0)]}):_0x4c4b70[_0x1778cc(0x1a0)]=_0x30fd9c,this[_0x1778cc(0x1a6)]({'load_last_search':'1'});}this['set']('form_trait',_0x4c4b70,{'silent':!![]});},'get_search_item_id'(){const _0x5e07fe=_0x374b79;let _0x255f4b=this[_0x5e07fe(0x1b3)]('search_item_id');return _0x255f4b+=0x1,this[_0x5e07fe(0x1b1)]('search_item_id',_0x255f4b),_0x255f4b;},'get_custom_props'(){const _0x399723=_0x374b79;return this[_0x399723(0x1b3)]('form_trait')||'{}';},'_get_last_search_info'(){const _0x16c01e=_0x374b79;let _0x245608=this[_0x16c01e(0x19a)]();if(_0x245608){let _0x9a0518=this['get']('attributes')[_0x16c01e(0x1a0)];return _0x245608['get_last_group_search_info'](_0x9a0518);}return{};},'get_last_search'(_0x289f1f){const _0x463898=_0x374b79;let _0x3beaa3=this[_0x463898(0x19f)]();if(_0x3beaa3)return _0x3beaa3['search_infos'][_0x289f1f];return null;},'load_last_search'(){const _0x4dbfb2=_0x374b79;let _0x515b48=this[_0x4dbfb2(0x1b3)]('attributes')['load_last_search'];return _0x515b48=='0'?![]:!![];return![];}},{'isComponent':_0x3fb41f=>{const _0x200701=_0x374b79;if(_0x3fb41f&&_0x3fb41f['classList']&&_0x3fb41f[_0x200701(0x1b4)]['contains']('search_group'))return{'type':'search_group'};}}),'view':_0x529e69['extend']({'events':{'click .search_button':'_onSearchButtonClick'},'init'(){const _0x14dcb1=_0x374b79;_0x529e69['prototype'][_0x14dcb1(0x1c2)][_0x14dcb1(0x1ae)](this,arguments),this['el']['addEventListener']('mana_dashboard.search_item_changed',this[_0x14dcb1(0x1b2)][_0x14dcb1(0x1a4)](this));},'_onSearchItemChanged'(){const _0x5d88bb=_0x374b79;let _0x1f89b5=this[_0x5d88bb(0x1aa)][_0x5d88bb(0x1b3)]('form_trait');if(!_0x1f89b5['keys']){let _0x3f8bf9=![];this[_0x5d88bb(0x1af)]['find']('.search_button')[_0x5d88bb(0x1b0)]==0x0&&(_0x3f8bf9=!![]),_0x1f89b5={'search_immidiate':_0x3f8bf9};}let _0x205971=_0x1f89b5[_0x5d88bb(0x1b8)];if(!_0x205971)return;this[_0x5d88bb(0x1bf)]();},'get_search_group_info'(){const _0x1b32f3=_0x374b79,_0x12e3c4=this[_0x1b32f3(0x1af)][_0x1b32f3(0x1b5)]('.search_item');let _0x3df23b={};for(let _0x56b40d=0x0;_0x56b40d<_0x12e3c4[_0x1b32f3(0x1b0)];_0x56b40d++){const _0x3b6522=_0x12e3c4[_0x56b40d];let _0x3ed196=grapesjs['$'](_0x3b6522)[_0x1b32f3(0x1c0)]('model');if(_0x3ed196){let _0x487e2f=_0x3ed196[_0x1b32f3(0x1bb)]();if(_0x487e2f){let _0x11aa7b=_0x487e2f[_0x1b32f3(0x193)];if(!_0x11aa7b)continue;_0x3df23b[_0x11aa7b]=_0x487e2f;}}}let _0x3d5aa2=this[_0x1b32f3(0x1aa)]['get']('form_trait');return{'targets':_0x3d5aa2[_0x1b32f3(0x196)]||[],'type':_0x3d5aa2['type']||'global','search_infos':_0x3df23b,'name':_0x3d5aa2[_0x1b32f3(0x1a0)]||'','is_global':_0x3d5aa2[_0x1b32f3(0x1be)]||![]};},'_onSearchButtonClick'(_0x118a46){const _0x10055b=_0x374b79,_0x473e74=$(_0x118a46[_0x10055b(0x1a9)]);if(!this['el'][_0x10055b(0x1c3)](_0x473e74[0x0]))return;let _0x4ffe49=grapesjs['$'](_0x118a46[_0x10055b(0x1ad)])[_0x10055b(0x1c0)]('model'),_0x5c8ff2=_0x4ffe49[_0x10055b(0x1b3)]('attributes')[_0x10055b(0x197)];_0x5c8ff2=='Reset'&&this[_0x10055b(0x18f)](),this['_do_search']();},'_reset_search'(){const _0x12258d=_0x374b79,_0x2ae5bd=this[_0x12258d(0x1af)][_0x12258d(0x1b5)]('.search_item');for(let _0x3c741d=0x0;_0x3c741d<_0x2ae5bd[_0x12258d(0x1b0)];_0x3c741d++){const _0x31d7d3=_0x2ae5bd[_0x3c741d];let _0x3bed6f=grapesjs['$'](_0x31d7d3)['data']('model');_0x3bed6f&&_0x3bed6f[_0x12258d(0x1b6)]();}},'_do_search'(){let _0xe6866e=this['get_widget']();_0xe6866e&&_0xe6866e['trigger_up']('mana_dashboard.do_search');}})});}return _0x327566['add']('search_group',_0x4663cb),_0x4663cb;}));function a0_0x1248(_0x17f0c4,_0x4c1d5a){const _0x364099=a0_0x3640();return a0_0x1248=function(_0x124817,_0x4d3801){_0x124817=_0x124817-0x18f;let _0x5946cc=_0x364099[_0x124817];return _0x5946cc;},a0_0x1248(_0x17f0c4,_0x4c1d5a);}function a0_0x3640(){const _0x49b615=['addType','40QhZfQL','key','6630vhPOGF','listenTo','targets','type','get_search_group_info','1243963bxKcRL','get_widget','load_last_search','10192853uRWasQ','3226VpTllR','extend','_get_last_search_info','name','prototype','29qzBRSB','BlockManager','bind','</div><div\x20class=\x27anita-block-label\x27>Group</div></div>','addAttributes','2329074SZjhng','1071456InKNWV','currentTarget','model','DomComponents','search_group_svg','target','apply','$el','length','set','_onSearchItemChanged','get','classList','find','resetSearch','view','search_immidiate','add','initialize','getSearchInfo','92zmcBbp','317358jCIXQu','is_global','_do_search','data','on_form_trait_change','init','contains','_reset_search','190jNICga'];a0_0x3640=function(){return _0x49b615;};return a0_0x3640();}