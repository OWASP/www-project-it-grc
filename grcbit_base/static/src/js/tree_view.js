odoo.define('grcbit.tree_view', function (require) {
"use strict";

    var ListRenderer = require('web.ListRenderer');
    var _t = require("web.core")._t;

    ListRenderer.include({
        events: _.extend({}, ListRenderer.prototype.events, {
            'click .o_external_button': '_onExternalButtonClicked',
        }),
        _onExternalButtonClicked: function(ev){
            ev.preventDefault();
            ev.stopPropagation();

            var this_button = $(ev.currentTarget);
            this_button.parent().parent().parent().click();
        },
        _renderExternalLinkHeader: function(){
            var $content = $('<div/>', {
            });

            return $('<th>')
            .addClass('o_list_record_selector')
            .append($content);
        },
        _renderExternalLink: function (url) {
            var $content = $('<div/>', {
            });
            var $anchor = $('<a/>', {
                href: url,
                class: 'fa fa-external-link o_external_button',
            });
            $content.append($anchor);

            return $('<td>')
            .addClass('o_list_record_selector')
            .append($content);
        },
        _renderRow: function (record) {
            var $tr = this._super.apply(this, arguments);
            if (this.hasSelectors) {
                var queryString = window.location.hash.substring(1);
                var urlParams = new URLSearchParams(queryString);
                var menuId = urlParams.get('menu_id') || '';
                var action = urlParams.get('action') || '';
                var model = this.state.model;


                var url = '#id=' + record.res_id + '&model=' + model + '&menu_id=' + menuId + '&action=' + action + '&view_type=form';
                
                $tr.prepend(this._renderExternalLink(url));
            }            

            return $tr;
        },

        _renderHeader: function () {
            var $tr = $('<tr>')
                .append(_.map(this.columns, this._renderHeaderCell.bind(this)));
            if (this.hasSelectors) {
                $tr.prepend(this._renderSelector('th'));
                $tr.prepend(this._renderExternalLinkHeader());
            }
            return $('<thead>').append($tr);
        },

        _renderFooter: function () {
            var aggregates = {};
            _.each(this.columns, function (column) {
                if ('aggregate' in column) {
                    aggregates[column.attrs.name] = column.aggregate;
                }
            });
            var $cells = this._renderAggregateCells(aggregates);
            if (this.hasSelectors) {
                $cells.unshift($('<td>'));
                $cells.unshift($('<td>'));
            }
            return $('<tfoot>').append($('<tr>').append($cells));
        },

        _renderGroupRow: function (group, groupLevel) {
            var cells = [];
            cells.push($('<td>'));

            var name = group.value === undefined ? _t('Undefined') : group.value;
            var groupBy = this.state.groupedBy[groupLevel];
            if (group.fields[groupBy.split(':')[0]].type !== 'boolean') {
                name = name || _t('Undefined');
            }
            var $th = $('<th>')
                .addClass('o_group_name')
                .attr('tabindex', -1)
                .text(name + ' (' + group.count + ')');
            var $arrow = $('<span>')
                .css('padding-left', 2 + (groupLevel * 20) + 'px')
                .css('padding-right', '5px')
                .addClass('fa');
            if (group.count > 0) {
                $arrow.toggleClass('fa-caret-right', !group.isOpen)
                    .toggleClass('fa-caret-down', group.isOpen);
            }
            $th.prepend($arrow);
            cells.push($th);

            var aggregateKeys = Object.keys(group.aggregateValues);
            var aggregateValues = _.mapObject(group.aggregateValues, function (value) {
                return { value: value };
            });
            var aggregateCells = this._renderAggregateCells(aggregateValues);
            var firstAggregateIndex = _.findIndex(this.columns, function (column) {
                return column.tag === 'field' && _.contains(aggregateKeys, column.attrs.name);
            });
            var colspanBeforeAggregate;
            if (firstAggregateIndex !== -1) {
                // if there are aggregates, the first $th goes until the first
                // aggregate then all cells between aggregates are rendered
                colspanBeforeAggregate = firstAggregateIndex;
                var lastAggregateIndex = _.findLastIndex(this.columns, function (column) {
                    return column.tag === 'field' && _.contains(aggregateKeys, column.attrs.name);
                });
                cells = cells.concat(aggregateCells.slice(firstAggregateIndex, lastAggregateIndex + 1));
                var colSpan = this.columns.length - 1 - lastAggregateIndex;
                if (colSpan > 0) {
                    cells.push($('<th>').attr('colspan', colSpan));
                }
            } else {
                var colN = this.columns.length;
                colspanBeforeAggregate = colN > 1 ? colN - 1 : 1;
                if (colN > 1) {
                    cells.push($('<th>'));
                }
            }
            if (this.hasSelectors) {
                colspanBeforeAggregate += 1;
            }
            $th.attr('colspan', colspanBeforeAggregate);

            if (group.isOpen && !group.groupedBy.length && (group.count > group.data.length)) {
                const lastCell = cells[cells.length - 1][0];
                this._renderGroupPager(group, lastCell);
            }
            if (group.isOpen && this.groupbys[groupBy]) {
                var $buttons = this._renderGroupButtons(group, this.groupbys[groupBy]);
                if ($buttons.length) {
                    var $buttonSection = $('<div>', {
                        class: 'o_group_buttons',
                    }).append($buttons);
                    $th.append($buttonSection);
                }
            }
            return $('<tr>')
                .addClass('o_group_header')
                .toggleClass('o_group_open', group.isOpen)
                .toggleClass('o_group_has_content', group.count > 0)
                .data('group', group)
                .append(cells);
        },

        _getNumberOfCols: function () {
            var n = this.columns.length;
            return this.hasSelectors ? n + 2 : n;
        },
    });

});



