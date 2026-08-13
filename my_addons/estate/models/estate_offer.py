from odoo import api, fields, models
from datetime import timedelta


class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "estate.offer"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("real.estate", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for rec in self:
            base_date = (
                rec.create_date.date() if rec.create_date else fields.Date.today()
            )
            rec.date_deadline = base_date + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            if rec.date_deadline:
                base_date = (
                    rec.create_date.date() if rec.create_date else fields.Date.today()
                )
                # Subtract dates to get the difference in days
                rec.validity = (rec.date_deadline - base_date).days
