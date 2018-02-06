# -*- coding: utf-8 -*-

from odoo import models, api


class RDUsers(models.Model):
    _inherit = 'res.users'

    @api.multi
    def create_alias(self):
        for user in self:
            alias_model_id = self.env["ir.model"].search([('model', '=', 'res.users')]).id

            if "@" in user.login:
                alias = user.login.split("@")[0]
            else:
                alias = user.login

            alias_obj = self.env["mail.alias"].search([('alias_name', '=', alias)])

            if alias_obj:
                alias_obj.write({'alias_model_id': alias_model_id,
                                 'alias_force_thread_id': user.id,
                                 'alias_user_id': user.id,
                                 'alias_parent_model_id': alias_model_id,
                                 'alias_parent_thread_id': user.id
                                 })
                user.write({"alias_id": alias_obj.id})
            else:
                new_alias = self.env['mail.alias'].create({'alias_name': alias,
                                                           'alias_model_id': alias_model_id,
                                                           'alias_force_thread_id': user.id,
                                                           'alias_user_id': user.id,
                                                           'alias_parent_model_id': alias_model_id,
                                                           'alias_parent_thread_id': user.id
                                                           })
                user.write({"alias_id": new_alias.id})

            user.partner_id.active = True
            user.message_post(body="Su correo electronico ha sido activado, su correo electronico es {}@{}".format(user.alias_id.alias_name,user.alias_id.alias_domain))

    @api.multi
    def disable_alias(self):
        for user in self:
            user.alias_id.write({'alias_force_thread_id': False,
                                 'alias_user_id': False,
                                 'alias_parent_model_id': False,
                                 'alias_parent_thread_id': False
                                 })
            user.write({"alias_id": False})

