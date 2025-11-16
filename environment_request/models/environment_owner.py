from odoo import _, api, fields, models
from odoo.exceptions import UserError




class EnvironmentOwner(models.Model):
    _name = "environment.owner"
    _description = "Solicitud de alta de entorno Odoo"
    _inherit = ["mail.thread", "mail.activity.mixin"]


    name = fields.Char(
        string="Referencia",
        default="New",
        readonly=True,
        copy=False,
        tracking=True,
        )


    state = fields.Selection(
    [
    ("draft", "Borrador"),
    ("requested", "Solicitado"),
    ("active", "Activo"),
    ("rejected", "Rechazado"),
    ("dropped", "Baja"),
    ],
    string="Estado",
    default="draft",
    tracking=True,
    )


    # create_date viene de base, lo usamos tal cual


    date_from = fields.Date(string="Desde", tracking=True)
    date_to = fields.Date(string="Hasta", tracking=True)


    environment_type = fields.Selection(
    [
    ("demo", "Demo"),
    ("production", "Producción"),
    ("development", "Desarrollo"),
    ],
    string="Tipo de entorno",
    required=True,
    tracking=True,
    )


    environment_version_id = fields.Many2one(
    comodel_name="environment.versions",
    string="Versión de Odoo",
    required=True,
    tracking=True,
    )


    customer_id = fields.Many2one(
    comodel_name="res.partner",
    string="Cliente",
    domain=[("is_company", "=", True)],
    tracking=True,
    )


    user_id = fields.Many2one(
    comodel_name="res.users",
    string="Responsable",
    default=lambda self: self.env.user,
    tracking=True,
    )


    is_custom_ip = fields.Boolean(string="IP personalizada")
    custom_ip = fields.Char(string="IP", tracking=True)


    is_custom_port = fields.Boolean(string="Puerto personalizado")
    custom_port = fields.Char(string="Puerto", tracking=True)


    description = fields.Html(string="Descripción / Alcance")


    @api.model
    def create(self, vals):
        if not vals.get("name") or vals.get("name") == "New":
            vals["name"] = (
            self.env["ir.sequence"].next_by_code("environment.owner") or _("New")
            )
        return super().create(vals)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _notify_environment_channel(self, action_key):
        """Send a message to the environment request channel.

        action_key: 'requested' | 'dropped'
        """
        channel = self.env.ref(
            "environment_request.env_channel_environment_requests",
            raise_if_not_found=False
        )
        if not channel:
            return

        for record in self:
            if action_key == "requested":
                action_label = _("Solicitada")
            elif action_key == "dropped":
                action_label = _("Eliminado")
            else:
                action_label = action_key

            body = _(
                "Solicitud de entorno: %(name)s . Para el cliente: %(customer)s fue %(action)s.",
                name=record.name,
                customer=record.customer_id.display_name or _("(no customer)"),
                action=action_label,
            )
            channel.sudo().message_post(
                body=body,
                message_type="comment",
                subtype_xmlid="mail.mt_comment",
            )

    # -------------------------------------------------------------------------
    # Buttons
    # -------------------------------------------------------------------------
    def action_draft(self):
        for rec in self:
            if rec.state == "requested":
                rec.state = "draft"

    def action_request_env(self):
        """User requests the environment.

        Only allowed from 'draft' or 'rejected'.
        Also notifies the channel.
        """
        for record in self:
            if record.state not in ("draft", "rejected"):
                raise UserError(
                    _(
                        "You can only request an environment from Draft or Rejected status."
                    )
                )
            record.state = "requested"
        self._notify_environment_channel("requested")
        return True

    def action_confirm_env(self):
        """Admin confirms/activates the environment.

        Only allowed from 'requested'.
        """
        for record in self:
            if record.state != "requested":
                raise UserError(_("Only requested environments can be confirmed."))
            record.state = "active"
        return True

    def action_cancel_env(self):
        """Admin cancels the request.

        Moves it to 'rejected'.
        """
        for record in self:
            if record.state not in ("draft", "requested"):
                raise UserError(
                    _("Only draft or requested environments can be cancelled.")
                )
            record.state = "rejected"
        return True

    def action_drop_env(self):
        """Admin drops an active environment.

        Only allowed from 'active'.
        Also notifies the channel.
        """
        for record in self:
            if record.state != "active":
                raise UserError(_("Only active environments can be dropped."))
            record.state = "dropped"
        self._notify_environment_channel("dropped")
        return True