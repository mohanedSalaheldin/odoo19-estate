from odoo import api, fields, models
from datetime import timedelta


class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "estate.offer"

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]
    _order = "price desc"

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
                base_date = (rec.create_date.date() if rec.create_date else fields.Date.today())
                rec.validity = (rec.date_deadline - base_date).days

    def action_accept(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True