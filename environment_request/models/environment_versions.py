from odoo import fields, models


class EnvironmentVersions(models.Model):
    _name = "environment.versions"
    _description = "Versiones de Odoo para entornos"

    # -------------------------------------------------------------------------
    # Fields
    name = fields.Char(string="Versión", required=True)