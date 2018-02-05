# -*- coding: utf-8 -*-
from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class product_product(models.Model):
    _inherit = 'product.product'


    @api.multi
    def update_pos_cache(self):
        pos_cache = self.env["pos.auto.cache"]
        use_redis, redis_db_pos = pos_cache.get_config()
        if use_redis:
            pos_cache.with_delay()._auto_cache_data("product_product", self.ids, sigle_cache=True)


    @api.model
    def create(self, vals):
        product = super(product_product, self).create(vals)
        notifications = []
        if product.sale_ok and product.available_in_pos:
            product_fields = self.env['product.product'].fields_get()
            product_fields_load = []
            for k, v in product_fields.iteritems():
                if v['type'] not in ['one2many', 'binary', 'monetary']:
                    product_fields_load.append(k)
            product_datas = product.sudo().read(product_fields_load)[0]
            product_datas['price'] = product_datas['list_price']
            product_datas['model'] = 'product.product'
            notifications.append([(self._cr.dbname, 'pos.sync.backend', self.env.user.id), product_datas])
        if notifications:
            _logger.info('===> sending')
            self.env['bus.bus'].sendmany(notifications)
        product.update_pos_cache()
        return product


class product_template(models.Model):
    _inherit = "product.template"

    not_returnable = fields.Boolean('No retornable')

    @api.multi
    def write(self, vals):
        res = super(product_template, self).write(vals)
        notifications = []
        product_fields = self.env['product.product'].fields_get()
        product_fields_load = []
        for k, v in product_fields.iteritems():
            if v['type'] not in ['one2many', 'binary', 'monetary']:
                product_fields_load.append(k)
        for product in self:
            products = self.env['product.product'].search([('product_tmpl_id', '=', product.id)])
            products.update_pos_cache()
            for p in products:
                if p and p.sale_ok and p.available_in_pos:
                    product_datas = p.sudo().read(product_fields_load)[0]
                    product_datas['price'] = product_datas['list_price']
                    product_datas['model'] = 'product.product'
                    notifications.append([(self._cr.dbname, 'pos.sync.backend', self.env.user.id), product_datas])
                    # notifications.append([(self._cr.dbname, 'pos.sync.backend', 100), product_datas])
                    # notifications.append([u"('{}', 'pos.sync.backend', '100')".format(self._cr.dbname) , product_datas])
        if notifications:
            _logger.info('===> sending')
            self.env['bus.bus'].sendmany(notifications)
        return res
