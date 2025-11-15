# -*- coding: utf-8 -*-
{
    "name": "Environment Requests Management",
    "summary": "Gestión de solicitudes de alta de entornos Odoo (demo, producción, desarrollo)",
    "version": "17.0.1.0.0",
    "author": "Ybaceta Fabrizio",
    "website": "https://www.linkedin.com/in/fybaceta/",
    "category": "Tools",
    "license": "LGPL-3",
    "depends": [
        "base",
        "mail",
        ],
    "data": [
        "security/environment_security.xml",
        "security/ir.model.access.csv",
        "data/environment_sequence.xml",
        "data/environment_versions_data.xml",
        "data/environment_channel_data.xml",
        "views/environment_menus.xml",
        "views/environment_owner_views.xml",
        "views/environment_versions_views.xml",
        "views/environment_config_views.xml",
    ],
"application": True,
}