odoo.define('ncf_pos_premium.popups', function (require) {
    "use strict";

    var PopupWidget = require('point_of_sale.popups');
    var gui = require('point_of_sale.gui');

    var MyMessagePopup = PopupWidget.extend({
        template: 'MyMessagePopup'
    });
    gui.define_popup({name: 'my_message', widget: MyMessagePopup});

    var OrderReturnPopup = PopupWidget.extend({
        template: 'OrderReturnPopup',
        events: {
            'click .button.cancel': 'click_cancel',
            'click #complete_return': 'click_complete_return',
            'click #return_order': 'click_return_order',
        },
        click_return_order: function () {
            var self = this;
            var all = $('.return_qty');
            var return_dict = {};
            var return_entries_ok = true;
            $.each(all, function (index, value) {
                var input_element = $(value).find('input');
                var line_quantity_remaining = parseFloat(input_element.attr('line-qty-remaining'));
                var line_id = parseFloat(input_element.attr('line-id'));
                var qty_input = parseFloat(input_element.val());
                if (!$.isNumeric(qty_input) || qty_input > line_quantity_remaining || qty_input < 0) {
                    return_entries_ok = false;
                    input_element.css("background-color", "#ff8888;");
                    setTimeout(function () {
                        input_element.css("background-color", "");
                    }, 100);
                    setTimeout(function () {
                        input_element.css("background-color", "#ff8888;");
                    }, 200);
                    setTimeout(function () {
                        input_element.css("background-color", "");
                    }, 300);
                    setTimeout(function () {
                        input_element.css("background-color", "#ff8888;");
                    }, 400);
                    setTimeout(function () {
                        input_element.css("background-color", "");
                    }, 500);
                }

                if (qty_input == 0 && line_quantity_remaining != 0 && !self.options.is_partial_return)
                    self.options.is_partial_return = true;
                else if (qty_input > 0) {
                    return_dict[line_id] = qty_input;
                    if (line_quantity_remaining != qty_input && !self.options.is_partial_return)
                        self.options.is_partial_return = true;
                    else if (!self.options.is_partial_return)
                        self.options.is_partial_return = false;
                }
            });
            if (return_entries_ok)
                self.create_return_order(return_dict);
        },
        create_return_order: function (return_dict) {
            var self = this;
            var order = self.options.order;
            var orderlines = self.options.orderlines;
            var current_order = self.pos.get_order();
            if (Object.keys(return_dict).length > 0) {
                self.chrome.widget.order_selector.neworder_click_handler();
                var refund_order = self.pos.get_order();
                refund_order.set_client(self.pos.db.get_partner_by_id(order.partner_id[0]));
                Object.keys(return_dict).forEach(function (line_id) {
                    var line = self.pos.db.line_by_id[line_id];
                    var product = self.pos.db.get_product_by_id(line.product_id[0]);
                    refund_order.add_product(product, {
                        quantity: parseFloat(return_dict[line_id]),
                        price: line.price_unit,
                        discount: line.discount
                    });
                    refund_order.selected_orderline.original_line_id = line.id;
                });
                if (self.options.is_partial_return) {
                    refund_order.set_return_status('Partially-Returned');
                    refund_order.set_return_order_id(order.id);
                    refund_order.set_is_return_order(true);
                } else {
                    refund_order.set_return_status('Fully-Returned');
                    refund_order.set_return_order_id(order.id);
                    refund_order.set_is_return_order(true);
                }
                self.pos.set_order(current_order);
                self.pos.set_order(refund_order);
                self.gui.show_screen('payment');
            }
            else {
                self.$("input").css("background-color", "#ff8888;");
                setTimeout(function () {
                    self.$("input").css("background-color", "");
                }, 100);
                setTimeout(function () {
                    self.$("input").css("background-color", "#ff8888;");
                }, 200);
                setTimeout(function () {
                    self.$("input").css("background-color", "");
                }, 300);
                setTimeout(function () {
                    self.$("input").css("background-color", "#ff8888;");
                }, 400);
                setTimeout(function () {
                    self.$("input").css("background-color", "");
                }, 500);
            }
        },
        click_complete_return: function () {
            var all = $('.return_qty');
            $.each(all, function (index, value) {
                var line_quantity_remaining = parseFloat($(value).find('input').attr('line-qty-remaining'));
                $(value).find('input').val(line_quantity_remaining);
            });
        },
        show: function (options) {
            options = options || {};
            this._super(options);
            this.orderlines = options.orderlines || [];
            this.renderElement();
        }
    });

    gui.define_popup({name: 'return_products_popup', widget: OrderReturnPopup});

    var PaymentScreenTextInput = PopupWidget.extend({
        template: 'PaymentScreenTextInput',
        show: function (options) {
            window.document.body.removeEventListener('keypress', this.gui.current_screen.keyboard_handler);
            window.document.body.removeEventListener('keydown', this.gui.current_screen.keyboard_keydown_handler);
            options = options || {};
            this._super(options);

            this.renderElement();
            this.$('input,textarea').focus();

        },
        click_cancel: function () {
            window.document.body.addEventListener('keypress', this.gui.current_screen.keyboard_handler);
            window.document.body.addEventListener('keydown', this.gui.current_screen.keyboard_keydown_handler);
            this.gui.close_popup();
            if (this.options.cancel) {
                this.options.cancel.call(this);
            }
        },
        click_confirm: function () {
            window.document.body.addEventListener('keypress', this.gui.current_screen.keyboard_handler);
            window.document.body.addEventListener('keydown', this.gui.current_screen.keyboard_keydown_handler);
            var value = this.$('input,textarea').val();
            this.gui.close_popup();
            if (this.options.confirm) {
                this.options.confirm.call(this, value);
            }
        }
    });

    gui.define_popup({name: 'payment_screen_text_input', widget: PaymentScreenTextInput});
});