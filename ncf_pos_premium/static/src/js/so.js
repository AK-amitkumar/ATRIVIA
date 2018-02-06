odoo.define('ecom_to_pos_sync', function (require) {
    var exports = {};
    var Backbone = window.Backbone;
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');
    var bus = require('bus.bus');
    var gui = require('point_of_sale.gui');
    var core = require('web.core');
    var Model = require('web.DataModel');
    var QWeb = core.qweb;
    var _t = core._t;

    var SaleOrderListScreenWidget = screens.ScreenWidget.extend({
        template: 'SaleOrderListScreenWidget',

        auto_back: true,
        renderElement: function () {
            var self = this;
            this._super();
            this.$('.back').click(function () {
                self.gui.back();
            });

            var search_timeout = null;
            this.$('.searchbox input').on('keyup', function (event) {
                var query = this.value;
                if (query == "") {
                    self.render_list(self.pos.sale_order_data);
                }
                else {
                    self.perform_search(query);
                }
            });
            this.$('.wv-order-list-contents').delegate('.wv_process_order_button', 'click', function (event) {
                var wv_order = self.get_order_by_id($(this).data('id'));
                var order = self.pos.get_order();
                var orderlines = order.get_orderlines();
                if (orderlines.length == 0) {
                    for (var j = 0; j < self.pos.sale_order_data.length; j++) {
                        if (self.pos.sale_order_data[j].id == wv_order.id) {
                            self.pos.sale_order_data.splice(j, 1);
                            self.pos.gui.screen_instances.products.action_buttons.Sale_Orde.renderElement();
                        }
                    }
                    order.set('client', undefined);
                    if (wv_order.partner_id) {
                        order.set_client(self.pos.db.get_partner_by_id(wv_order.partner_id));
                    }
                    for (var i = 0; i < wv_order.order_line.length; i++) {
                        var s_line = wv_order.order_line[i];
                        if (s_line) {
                            var product = self.pos.db.get_product_by_id(s_line.product_id);
                            order.add_product(product, {
                                'quantity': s_line.product_uom_qty,
                                'price': s_line.price_unit
                            });
                        }
                    }
                    self.gui.back();
                }
                else {
                    self.gui.show_popup('error', {
                        'title': 'Error: Could not Process Order',
                        'body': 'Please remove all products from cart and try again.',
                    });
                }
            });
        },
        show: function () {
            var self = this;
            this._super();
            this.renderElement();
            this.render_list(self.pos.sale_order_data);
        },

        perform_search: function (query) {

            var orders = this.pos.sale_order_data;
            var results = [];
            for (var i = 0; i < orders.length; i++) {
                var res = this.search_orders(query, orders[i]);
                if (res != false) {
                    results.push(res);
                }
            }
            this.render_list(results);
        },
        search_orders: function (query, orders) {
            try {
                query = query.replace(/[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g, '.');
                query = query.replace(' ', '.+');
                var re = RegExp("([0-9]+):.*?" + query, "gi");
            } catch (e) {
                return [];
            }
            var results = [];
            var r = re.exec(this._order_search_string(orders));
            if (r) {
                var id = Number(r[1]);
                return this.get_order_by_id(id);
            }
            return false;
        },
        get_order_by_id: function (id) {
            var orders = this.pos.sale_order_data;
            for (var i = 0; i < orders.length; i++) {
                if (orders[i].id == id) {
                    return orders[i];
                }
            }
        },
        _order_search_string: function (order) {
            var str = order.name;

            if (order.partner_id) {
                str += '|' + order.partner_name;
            }
            str = '' + order.id + ':' + str.replace(':', '') + '\n';
            return str;
        },
        render_list: function (orderVal) {
            var self = this;
            var contents = this.$el[0].querySelector('.wv-order-list-contents');
            contents.innerHTML = "";
            var orders = orderVal;
            for (var i = 0; i < orders.length; i++) {
                var order = orders[i];
                var clientline_html = QWeb.render('SaleOrderLine', {widget: self, order: order});
                var clientline = document.createElement('tbody');
                clientline.innerHTML = clientline_html;
                clientline = clientline.childNodes[1];
                contents.appendChild(clientline);
            }
        },

        close: function () {
            this._super();
        },
    });
    gui.define_screen({name: 'sale_order_list', widget: SaleOrderListScreenWidget});

    var SaleOrderButton = screens.ActionButtonWidget.extend({
        template: 'SaleOrderButton',
        ecom_orders: function () {
            if (this.pos.sale_order_data) {
                return this.pos.sale_order_data.length;
            } else {
                return 0;
            }
        },
        button_click: function () {
            this.gui.show_screen('sale_order_list', {}, 'refresh');
        },
    });
    screens.define_action_button({
        'name': 'Sale_Orde',
        'widget': SaleOrderButton,
        'condition': function () {
            return true;
        }
    });
});
