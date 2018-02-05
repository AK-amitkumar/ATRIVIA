# -*- coding: utf-8 -*-
###########################################################################
#    Copyright (C) 2017 - Today Almighty Consulting Services. <http://www.turkeshpatel.odoo.com>
#
#    @author Almighty Consulting Services (info@almightycs.com)
##############################################################################

{
    "name": "Project Gantt View",
    "version": "1.0",
    "author": "Almighty Consulting Services",
    "category": "Project",
    "description": """Odoo Project Web Gantt chart view.""",
    "summary": """Odoo Project Web Gantt chart view.""",
    "depends": ['web_gantt_view','project'],
    "data" : [
        'views/project_view.xml', 
    ],
    'images': [
         'static/description/gantt_view_turkeshpatel_almihgtycs.png',
     ],
    "auto_install": False,
    "installable": True,
    "price": 20,
    "currency": "EUR",
}
