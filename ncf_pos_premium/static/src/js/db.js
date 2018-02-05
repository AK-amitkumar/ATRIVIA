odoo.define('ncf_pos_premium.db', function (require) {
    "use strict";
    var pos_db = require('point_of_sale.DB');

    pos_db.include({
        _partner_search_string: function (partner) {
            var str = this._super(partner);
            str = str.replace('\n', '');
            if (partner.vat) {
                str += '|' + partner.vat;
            }
            return str + '\n';
        },
        is_product_in_category: function (category_ids, product_id) {
            try {
                return this._super(options);
            } catch (ex) {
                return false
            }
        }
    });
});
