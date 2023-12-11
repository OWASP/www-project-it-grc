odoo.define('mana_dashboard_gauge.gauge_chart', function (require) {
    "use strict";

    var BlockRegistry = require('mana_dashboard.block_registry');
    var builder = require('mana_dashboard.chart_builder');
    var icons = require('mana_dashboard.icons');

    var { render_block, default_chart_trait } = require('mana_dashboard.chart_util');

    var core = require('web.core');
    var _t = core._t;
    
    // gauge chart
    BlockRegistry.add('gauge_chart', builder({
        name: _t('Gauge Chart'),
        chart_type: 'gauge_chart',
        render: render_block('Gauge Chart', icons.gauge_chart_svg),
        default_option: {
            series: [
              {
                type: 'gauge',
                progress: {
                  show: true,
                  width: 18
                },
                axisLine: {
                  lineStyle: {
                    width: 18
                  }
                },
                axisTick: {
                  show: false
                },
                splitLine: {
                  length: 15,
                  lineStyle: {
                    width: 2,
                    color: '#999'
                  }
                },
                axisLabel: {
                  distance: 25,
                  color: '#999',
                  fontSize: 20
                },
                anchor: {
                  show: true,
                  showAbove: true,
                  size: 25,
                  itemStyle: {
                    borderWidth: 10
                  }
                },
                title: {
                  show: false
                },
                detail: {
                  valueAnimation: true,
                  fontSize: 80,
                  offsetCenter: [0, '70%']
                },
                data: [
                  {
                    value: 70
                  }
                ]
              }
            ]
        },
        traits: default_chart_trait,
        content: {
            type: 'gauge_chart',
        },
        category: _t('Chart'),
        isComponent(el) {
            if (el.classList && el.classList.contains('gauge_chart')) {
                return { type: 'gauge_chart' };
            }
        },
        default_template: 'mana_dashboard.template_simple_gauge_chart',
        template_category: 'chart',
        template_type: 'gauge chart',
        search_sensitive: true,
        enable_drill_down: false,
    }))

});