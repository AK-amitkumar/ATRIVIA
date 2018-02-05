# -*- coding: utf-8 -*-
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    allow_payments = fields.Boolean(u'Permitir pagos', default=True)
    allow_delete_order = fields.Boolean(u'Permitir eliminar ordenes no vacía', default=True)
    allow_add_order = fields.Boolean(u'Permitir crear ordenes', default=True)
    allow_discount = fields.Boolean(u'Permitir descuento', default=True)
    allow_edit_price = fields.Boolean(u'Permitir la edición del precio', default=True)
    allow_decrease_amount = fields.Boolean(u'Permitir la edición de la cantidad', default=True)
    allow_delete_order_line = fields.Boolean(u'Permitir eliminar línea de pedido', default=True)
    allow_create_order_line = fields.Boolean(u'Permitir crear línea de pedido', default=True)
    allow_refund_order = fields.Boolean(u'Permitir crear notas de crédito', default=True)
