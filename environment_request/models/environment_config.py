from odoo import fields, models


class EnvironmentConfig(models.Model):
    _name = "environment.config"
    _description = "Configuraciones de gestión de entornos"


    name = fields.Char(string="Nombre", required=True)


    default_environment_type = fields.Selection(
        [
        ("demo", "Demo"),
        ("production", "Producción"),
        ("development", "Desarrollo"),
        ],
        string="Tipo de entorno por defecto",
        )


    default_environment_version_id = fields.Many2one(
    comodel_name="environment.versions",
    string="Versión Odoo por defecto",
    )


    notes = fields.Text(string="Notas")