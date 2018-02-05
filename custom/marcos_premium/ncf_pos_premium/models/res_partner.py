# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def update_pos_cache(self):
        pos_cache = self.env["pos.auto.cache"]
        use_redis, redis_db_pos = pos_cache.get_config()
        if use_redis:
            pos_cache.with_delay()._auto_cache_data("res_partner", self.ids, sigle_cache=True)

    @api.model
    def sending_notification(self, partner):
        notifications = []
        partner_fields = self.env['res.partner'].fields_get()
        partner_fields_load = []
        for k, v in partner_fields.iteritems():
            if v['type'] not in ['one2many', 'binary', 'monetary']:
                partner_fields_load.append(k)
        partner_datas = partner.sudo().read(partner_fields_load)[0]
        partner_datas['model'] = 'res.partner'
        notifications.append([(self._cr.dbname, 'pos.sync.backend', self.env.user.id), partner_datas])
        # notifications.append([u"('{}', 'pos.sync.backend', '100')".format(self._cr.dbname), partner_datas])
        if notifications:
            _logger.info('sending: %s' % notifications)
            self.env['bus.bus'].sendmany(notifications)

    @api.model
    def create(self, vals):
        partner = super(ResPartner, self).create(vals)
        if partner.customer == True:
            self.sending_notification(partner)
        self.update_pos_cache()
        return partner

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        for partner in self:
            if partner.customer == True:
                self.sending_notification(partner)
        self.update_pos_cache()
        return res

    @api.model
    def create_from_ui(self, partner):

        """ create or modify a partner from the point of sale ui.
            partner contains the partner's fields. """
        # image is a dataurl, get the data after the comma
        if partner.get('image'):
            partner['image'] = partner['image'].split(',')[1]
        partner_id = partner.pop('id', False)
        if partner_id:  # Modifying existing partner
            partner.pop('vat', None)
            self.browse(partner_id).write(partner)
        else:
            partner_id = self.create(partner).ids
        return partner_id


class account_journal(models.Model):
    _inherit = 'account.journal'

    credit = fields.Boolean(string='POS Credit Journal')
