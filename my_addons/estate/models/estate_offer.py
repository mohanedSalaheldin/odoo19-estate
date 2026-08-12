from odoo import fields, models


class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "estate.offer"

    price = fields.Float()
    status = fields.Selection(
        [
            ("accepted","Accepted"),
            ("refused","Refused"),
        ], 
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("real.estate", required=True)