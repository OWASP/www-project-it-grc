(function(_0x53449b,_0x36174e){const _0x258ea6=a0_0x36cb,_0x444357=_0x53449b();while(!![]){try{const _0x12ed63=parseInt(_0x258ea6(0x1ab))/0x1+parseInt(_0x258ea6(0x1a4))/0x2*(-parseInt(_0x258ea6(0x1a1))/0x3)+-parseInt(_0x258ea6(0x1a2))/0x4*(parseInt(_0x258ea6(0x19f))/0x5)+parseInt(_0x258ea6(0x1a0))/0x6*(parseInt(_0x258ea6(0x1a3))/0x7)+-parseInt(_0x258ea6(0x1a7))/0x8+-parseInt(_0x258ea6(0x19d))/0x9*(parseInt(_0x258ea6(0x1a9))/0xa)+parseInt(_0x258ea6(0x19c))/0xb*(parseInt(_0x258ea6(0x1ac))/0xc);if(_0x12ed63===_0x36174e)break;else _0x444357['push'](_0x444357['shift']());}catch(_0x57c508){_0x444357['push'](_0x444357['shift']());}}}(a0_0x1ce9,0x47126),odoo['define']('mana_dashboard.date_util',function(require){'use strict';const _0x5ce0ab=a0_0x36cb;const _0x53c2f3=require('web.core');function get_this_year(){const _0x4ec57f=a0_0x36cb;let _0x157005=moment(),_0x58b1c7=moment(_0x157005)[_0x4ec57f(0x1a8)]('year'),_0x32b9c8=moment(_0x157005)[_0x4ec57f(0x1a6)]('year');return[_0x58b1c7[_0x4ec57f(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x32b9c8[_0x4ec57f(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function get_this_month(){const _0x5b7659=a0_0x36cb;let _0x4ccf9b=moment(),_0x481107=moment(_0x4ccf9b)[_0x5b7659(0x1a8)]('month'),_0x51a115=moment(_0x4ccf9b)['endOf']('month');return[_0x481107['format']('YYYY-MM-DD HH:mm:ss'),_0x51a115['format']('YYYY-MM-DD HH:mm:ss')];}function get_this_week(){const _0x3781fb=a0_0x36cb;let _0x249944=moment(),_0x22b228=moment(_0x249944)[_0x3781fb(0x1a8)]('week'),_0x1d2164=moment(_0x249944)[_0x3781fb(0x1a6)]('week');return[_0x22b228[_0x3781fb(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x1d2164[_0x3781fb(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0xaef2ac(){const _0x2db421=a0_0x36cb;let _0x2582cb=moment(),_0x599b1e=moment(_0x2582cb)[_0x2db421(0x1a8)]('day'),_0x3bf268=moment(_0x2582cb)[_0x2db421(0x1a6)]('day');return[_0x599b1e[_0x2db421(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x3bf268[_0x2db421(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x4edd0e(){const _0x5cfdc5=a0_0x36cb;let _0x5e862f=moment(),_0x2d0b50=moment(_0x5e862f)['add'](0x1,'year')[_0x5cfdc5(0x1a8)]('year'),_0x19206e=moment(_0x5e862f)['add'](0x1,'year')['endOf']('year');return[_0x2d0b50['format']('YYYY-MM-DD HH:mm:ss'),_0x19206e[_0x5cfdc5(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0xb20fee(){const _0x2764e=a0_0x36cb;let _0x49e705=moment(),_0x47635d=moment(_0x49e705)[_0x2764e(0x19e)](0x1,'month')['startOf']('month'),_0x16b654=moment(_0x49e705)[_0x2764e(0x19e)](0x1,'month')[_0x2764e(0x1a6)]('month');return[_0x47635d[_0x2764e(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x16b654[_0x2764e(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x19e514(){const _0x1d884f=a0_0x36cb;let _0x55077a=moment(),_0x17d717=moment(_0x55077a)[_0x1d884f(0x19e)](0x1,'week')[_0x1d884f(0x1a8)]('week'),_0x4e6390=moment(_0x55077a)['add'](0x1,'week')[_0x1d884f(0x1a6)]('week');return[_0x17d717[_0x1d884f(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x4e6390['format']('YYYY-MM-DD HH:mm:ss')];}function _0x4d22fc(){const _0x569959=a0_0x36cb;let _0x33759d=moment(),_0x366de6=moment(_0x33759d)[_0x569959(0x19e)](0x1,'day')['startOf']('day'),_0x4da134=moment(_0x33759d)[_0x569959(0x19e)](0x1,'day')[_0x569959(0x1a6)]('day');return[_0x366de6[_0x569959(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x4da134[_0x569959(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x398e88(){const _0x3f0659=a0_0x36cb;let _0x173b16=moment(),_0x2a59c1=moment(_0x173b16)[_0x3f0659(0x1aa)](0x1,'year')[_0x3f0659(0x1a8)]('year'),_0x276f32=moment(_0x173b16)[_0x3f0659(0x1aa)](0x1,'year')[_0x3f0659(0x1a6)]('year');return[_0x2a59c1['format']('YYYY-MM-DD HH:mm:ss'),_0x276f32['format']('YYYY-MM-DD HH:mm:ss')];}function _0x766a62(){const _0x1c4a23=a0_0x36cb;let _0x1f696e=moment(),_0x225aa0=moment(_0x1f696e)['subtract'](0x1,'month')[_0x1c4a23(0x1a8)]('month'),_0x4ad8bf=moment(_0x1f696e)[_0x1c4a23(0x1aa)](0x1,'month')[_0x1c4a23(0x1a6)]('month');return[_0x225aa0['format']('YYYY-MM-DD HH:mm:ss'),_0x4ad8bf[_0x1c4a23(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x270e54(){const _0x1be03b=a0_0x36cb;let _0x172c0d=moment(),_0xc1eca4=moment(_0x172c0d)[_0x1be03b(0x1aa)](0x1,'week')[_0x1be03b(0x1a8)]('week'),_0x55d5fd=moment(_0x172c0d)[_0x1be03b(0x1aa)](0x1,'week')['endOf']('week');return[_0xc1eca4[_0x1be03b(0x1a5)]('YYYY-MM-DD'),_0x55d5fd[_0x1be03b(0x1a5)]('YYYY-MM-DD')];}function _0x264b79(){const _0x54f80f=a0_0x36cb;let _0x5b1e14=moment(),_0xdc6f53=moment(_0x5b1e14)[_0x54f80f(0x1aa)](0x1,'day')[_0x54f80f(0x1a8)]('day'),_0x4f678a=moment(_0x5b1e14)['subtract'](0x1,'day')[_0x54f80f(0x1a6)]('day');return[_0xdc6f53[_0x54f80f(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x4f678a[_0x54f80f(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x4d08c3(){const _0xcc2d61=a0_0x36cb;let _0x4cf95e=moment(),_0x43b090=moment(_0x4cf95e)[_0xcc2d61(0x1aa)](0x7,'day')[_0xcc2d61(0x1a8)]('day'),_0x49217d=moment(_0x4cf95e)[_0xcc2d61(0x1a6)]('day');return[_0x43b090[_0xcc2d61(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x49217d['format']('YYYY-MM-DD HH:mm:ss')];}function _0x1d5f4a(){const _0x587788=a0_0x36cb;let _0x8393de=moment(),_0x50fecf=moment(_0x8393de)[_0x587788(0x1aa)](0x1e,'day')[_0x587788(0x1a8)]('day'),_0xe3ac6d=moment(_0x8393de)['endOf']('day');return[_0x50fecf[_0x587788(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0xe3ac6d[_0x587788(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x546540(){const _0x1c0e18=a0_0x36cb;let _0x324d03=moment(),_0x258bc5=moment(_0x324d03)['subtract'](0x5a,'day')[_0x1c0e18(0x1a8)]('day'),_0x4a1061=moment(_0x324d03)[_0x1c0e18(0x1a6)]('day');return[_0x258bc5['format']('YYYY-MM-DD HH:mm:ss'),_0x4a1061[_0x1c0e18(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x31b189(){const _0x42486e=a0_0x36cb;let _0x41d44f=moment(),_0x491e14=moment(_0x41d44f)['subtract'](0x16d,'day')['startOf']('day'),_0x41ce67=moment(_0x41d44f)[_0x42486e(0x1a6)]('day');return[_0x491e14[_0x42486e(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x41ce67[_0x42486e(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x152fa2(){const _0x46876b=a0_0x36cb;let _0xa3338b=moment(),_0x172479=moment(_0xa3338b)[_0x46876b(0x1a8)]('day'),_0x134ef5=moment(_0xa3338b)[_0x46876b(0x19e)](0x7,'day')[_0x46876b(0x1a6)]('day');return[_0x172479['format']('YYYY-MM-DD HH:mm:ss'),_0x134ef5[_0x46876b(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x382bb9(){const _0x43ff51=a0_0x36cb;let _0x339117=moment(),_0x400a83=moment(_0x339117)['startOf']('day'),_0x412480=moment(_0x339117)['add'](0x1e,'day')[_0x43ff51(0x1a6)]('day');return[_0x400a83[_0x43ff51(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x412480['format']('YYYY-MM-DD HH:mm:ss')];}function _0x4b6d1e(){const _0x2bcb6e=a0_0x36cb;let _0x15f376=moment(),_0x4933fe=moment(_0x15f376)['startOf']('day'),_0x36cf6b=moment(_0x15f376)[_0x2bcb6e(0x19e)](0x5a,'day')[_0x2bcb6e(0x1a6)]('day');return[_0x4933fe[_0x2bcb6e(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x36cf6b[_0x2bcb6e(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x1c7ef4(){const _0x10bb1f=a0_0x36cb;let _0xde5f84=moment(),_0x3a5cba=moment(_0xde5f84)[_0x10bb1f(0x1a8)]('day'),_0xbdff02=moment(_0xde5f84)[_0x10bb1f(0x19e)](0x16d,'day')[_0x10bb1f(0x1a6)]('day');return[_0x3a5cba['format']('YYYY-MM-DD HH:mm:ss'),_0xbdff02[_0x10bb1f(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function get_this_month(){const _0x274122=a0_0x36cb;let _0x55a7bc=moment(),_0x49f507=moment(_0x55a7bc)[_0x274122(0x1a8)]('month'),_0x132ce5=moment(_0x55a7bc)[_0x274122(0x1a6)]('month');return[_0x49f507['format']('YYYY-MM-DD HH:mm:ss'),_0x132ce5[_0x274122(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function get_this_week(){const _0x2e8aea=a0_0x36cb;let _0x68a696=moment(),_0x863adf=moment(_0x68a696)[_0x2e8aea(0x1a8)]('week'),_0x5e7baf=moment(_0x68a696)[_0x2e8aea(0x1a6)]('week');return[_0x863adf[_0x2e8aea(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x5e7baf['format']('YYYY-MM-DD HH:mm:ss')];}function _0xaef2ac(){const _0x2af084=a0_0x36cb;let _0xaabdbd=moment(),_0x21c571=moment(_0xaabdbd)['startOf']('day'),_0x41b335=moment(_0xaabdbd)['endOf']('day');return[_0x21c571[_0x2af084(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x41b335['format']('YYYY-MM-DD HH:mm:ss')];}function get_this_quarter(){const _0x24c6f6=a0_0x36cb;let _0x36f2a4=moment(),_0x57619a=moment(_0x36f2a4)[_0x24c6f6(0x1a8)]('quarter'),_0x58c406=moment(_0x36f2a4)[_0x24c6f6(0x1a6)]('quarter');return[_0x57619a[_0x24c6f6(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x58c406[_0x24c6f6(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x249bf6(){const _0xf59284=a0_0x36cb;let _0x4f32c7=moment(),_0x429c2c=moment(_0x4f32c7)[_0xf59284(0x1aa)](0x1,'quarter')['startOf']('quarter'),_0x5d765c=moment(_0x4f32c7)['subtract'](0x1,'quarter')[_0xf59284(0x1a6)]('quarter');return[_0x429c2c['format']('YYYY-MM-DD HH:mm:ss'),_0x5d765c[_0xf59284(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x1fd9e3(){const _0x55120e=a0_0x36cb;let _0x67adad=moment(),_0x527b64=moment(_0x67adad)[_0x55120e(0x19e)](0x1,'quarter')[_0x55120e(0x1a8)]('quarter'),_0x5ff0e2=moment(_0x67adad)[_0x55120e(0x19e)](0x1,'quarter')[_0x55120e(0x1a6)]('quarter');return[_0x527b64[_0x55120e(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x5ff0e2[_0x55120e(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x4edd0e(){const _0x11cbe2=a0_0x36cb;let _0x3d0ae=moment(),_0x430815=moment(_0x3d0ae)[_0x11cbe2(0x19e)](0x1,'year')['startOf']('year'),_0x3d2d5f=moment(_0x3d0ae)[_0x11cbe2(0x19e)](0x1,'year')['endOf']('year');return[_0x430815[_0x11cbe2(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x3d2d5f['format']('YYYY-MM-DD HH:mm:ss')];}function _0x766a62(){const _0x1b7f31=a0_0x36cb;let _0x1bc3f2=moment(),_0x58f6a5=moment(_0x1bc3f2)[_0x1b7f31(0x1aa)](0x1,'month')['startOf']('month'),_0x6313b7=moment(_0x1bc3f2)[_0x1b7f31(0x1aa)](0x1,'month')[_0x1b7f31(0x1a6)]('month');return[_0x58f6a5[_0x1b7f31(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x6313b7[_0x1b7f31(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x270e54(){const _0x1c2a9e=a0_0x36cb;let _0x5c2ac5=moment(),_0x2a5041=moment(_0x5c2ac5)[_0x1c2a9e(0x1aa)](0x1,'week')[_0x1c2a9e(0x1a8)]('week'),_0x2f011a=moment(_0x5c2ac5)['subtract'](0x1,'week')['endOf']('week');return[_0x2a5041[_0x1c2a9e(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x2f011a[_0x1c2a9e(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x4d08c3(){const _0x574565=a0_0x36cb;let _0x253274=moment(),_0x196e40=moment(_0x253274)[_0x574565(0x1aa)](0x7,'day')[_0x574565(0x1a8)]('day'),_0x3ce253=moment(_0x253274)[_0x574565(0x1a6)]('day');return[_0x196e40[_0x574565(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x3ce253[_0x574565(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x1d5f4a(){const _0x330e00=a0_0x36cb;let _0x41e229=moment(),_0x1a932a=moment(_0x41e229)['subtract'](0x1e,'day')[_0x330e00(0x1a8)]('day'),_0x5c7d0b=moment(_0x41e229)['endOf']('day');return[_0x1a932a[_0x330e00(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x5c7d0b[_0x330e00(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x546540(){const _0x280e66=a0_0x36cb;let _0x437426=moment(),_0x6e8f4b=moment(_0x437426)[_0x280e66(0x1aa)](0x5a,'day')[_0x280e66(0x1a8)]('day'),_0x14fd65=moment(_0x437426)[_0x280e66(0x1a6)]('day');return[_0x6e8f4b[_0x280e66(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x14fd65[_0x280e66(0x1a5)]('YYYY-MM-DD HH:mm:ss')];}function _0x31b189(){const _0x4edd96=a0_0x36cb;let _0x457775=moment(),_0x156573=moment(_0x457775)[_0x4edd96(0x1aa)](0x16d,'day')[_0x4edd96(0x1a8)]('day'),_0x20c3c9=moment(_0x457775)['endOf']('day');return[_0x156573[_0x4edd96(0x1a5)]('YYYY-MM-DD HH:mm:ss'),_0x20c3c9['format']('YYYY-MM-DD HH:mm:ss')];}let _0x26009d={'All Time':[moment('2010-01-01'),moment('2050-12-31')],'This Year':[moment()[_0x5ce0ab(0x1a8)]('year'),moment()[_0x5ce0ab(0x1a6)]('year')],'This Month':[moment()[_0x5ce0ab(0x1a8)]('month'),moment()[_0x5ce0ab(0x1a6)]('month')],'This Week':[moment()[_0x5ce0ab(0x1a8)]('week'),moment()[_0x5ce0ab(0x1a6)]('week')],'Today':[moment()['startOf']('day'),moment()[_0x5ce0ab(0x1a6)]('day')],'This Quarter':[moment()[_0x5ce0ab(0x1a8)]('quarter'),moment()[_0x5ce0ab(0x1a6)]('quarter')],'Last Quarter':[moment()[_0x5ce0ab(0x1aa)](0x1,'quarter')[_0x5ce0ab(0x1a8)]('quarter'),moment()[_0x5ce0ab(0x1aa)](0x1,'quarter')['endOf']('quarter')],'Next Quarter':[moment()[_0x5ce0ab(0x19e)](0x1,'quarter')[_0x5ce0ab(0x1a8)]('quarter'),moment()[_0x5ce0ab(0x19e)](0x1,'quarter')[_0x5ce0ab(0x1a6)]('quarter')],'Next Year':[moment()[_0x5ce0ab(0x19e)](0x1,'year')[_0x5ce0ab(0x1a8)]('year'),moment()['add'](0x1,'year')[_0x5ce0ab(0x1a6)]('year')],'Last Month':[moment()[_0x5ce0ab(0x1aa)](0x1,'month')[_0x5ce0ab(0x1a8)]('month'),moment()['subtract'](0x1,'month')['endOf']('month')],'Last Week':[moment()[_0x5ce0ab(0x1aa)](0x1,'week')['startOf']('week'),moment()[_0x5ce0ab(0x1aa)](0x1,'week')[_0x5ce0ab(0x1a6)]('week')],'Last 7 Days':[moment()[_0x5ce0ab(0x1aa)](0x7,'day')[_0x5ce0ab(0x1a8)]('day'),moment()['endOf']('day')],'Last 30 Days':[moment()['subtract'](0x1e,'day')['startOf']('day'),moment()[_0x5ce0ab(0x1a6)]('day')],'Last 90 Days':[moment()['subtract'](0x5a,'day')['startOf']('day'),moment()[_0x5ce0ab(0x1a6)]('day')],'Last 365 Days':[moment()[_0x5ce0ab(0x1aa)](0x16d,'day')[_0x5ce0ab(0x1a8)]('day'),moment()[_0x5ce0ab(0x1a6)]('day')],'Next Month':[moment()[_0x5ce0ab(0x19e)](0x1,'month')[_0x5ce0ab(0x1a8)]('month'),moment()[_0x5ce0ab(0x19e)](0x1,'month')[_0x5ce0ab(0x1a6)]('month')],'Next Week':[moment()[_0x5ce0ab(0x19e)](0x1,'week')[_0x5ce0ab(0x1a8)]('week'),moment()['add'](0x1,'week')[_0x5ce0ab(0x1a6)]('week')],'Yesterday':[moment()[_0x5ce0ab(0x1aa)](0x1,'day')[_0x5ce0ab(0x1a8)]('day'),moment()[_0x5ce0ab(0x1aa)](0x1,'day')['endOf']('day')],'Tomorrow':[moment()['add'](0x1,'day')[_0x5ce0ab(0x1a8)]('day'),moment()[_0x5ce0ab(0x19e)](0x1,'day')['endOf']('day')]};return{'get_this_year':get_this_year,'get_this_month':get_this_month,'get_this_week':get_this_week,'get_today':_0xaef2ac,'get_yesterday':_0x264b79,'get_tomorrow':_0x4d22fc,'get_this_quarter':get_this_quarter,'get_last_quarter':_0x249bf6,'get_next_quarter':_0x1fd9e3,'get_next_year':_0x4edd0e,'get_next_month':_0xb20fee,'get_next_week':_0x19e514,'get_last_year':_0x398e88,'get_last_month':_0x766a62,'get_last_week':_0x270e54,'get_last_7_days':_0x4d08c3,'get_last_30_days':_0x1d5f4a,'get_last_90_days':_0x546540,'get_last_365_days':_0x31b189,'get_next_7_days':_0x152fa2,'get_next_30_days':_0x382bb9,'get_next_90_days':_0x4b6d1e,'get_next_365_days':_0x1c7ef4,'date_ranges':_0x26009d};}));function a0_0x36cb(_0x393af5,_0x147843){const _0x1ce955=a0_0x1ce9();return a0_0x36cb=function(_0x36cbcf,_0x3a3bee){_0x36cbcf=_0x36cbcf-0x19c;let _0x317643=_0x1ce955[_0x36cbcf];return _0x317643;},a0_0x36cb(_0x393af5,_0x147843);}function a0_0x1ce9(){const _0x13182f=['add','15715ZVziwl','12TJuihq','5937xjlhvw','568stnJdm','137767uPlcQR','548hxIRIR','format','endOf','2558944EKPLdz','startOf','3472270TUDpfe','subtract','280527MWXbJn','24ofdWNX','8947774OYrjNK','9gtEKiZ'];a0_0x1ce9=function(){return _0x13182f;};return a0_0x1ce9();}