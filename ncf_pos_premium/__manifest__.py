# -*- coding: utf-8 -*-
{
    'name': "ncf_pos_premium",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'bus', 'point_of_sale', 'ncf_manager', 'ipf_manager'],
    "external_dependencies": {"python": [], "bin": []},
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/pos_view.xml',
        'views/pos_sesion_view.xml',
        'views/pos_config_view.xml',
        'data/data.xml',
        'views/res_partner_view.xml',
        'views/res_users_view.xml',
        'views/pos_bus_view.xml',
        'views/restaurant.xml',
        'views/templates.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [

        'static/src/xml/action_pad.xml',
        'static/src/xml/client.xml',
        'static/src/xml/payment.xml',
        'static/src/xml/popup.xml',
        'static/src/xml/pos_order.xml',
        'static/src/xml/pos_orders.xml',
        'static/src/xml/pos_ticket.xml',
        'static/src/xml/bus.xml',
        'static/src/xml/restaurant.xml',
        # 'static/src/xml/so.xml',
    ],

    "post_load": None,
    "pre_init_hook": None,
    "post_init_hook": None,

    "auto_install": False,
    "installable": True,
}
