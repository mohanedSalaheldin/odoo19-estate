from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import fields, models


class RealEstate(models.Model):
    _name = "real.estate"
    _description = "estate.estate"

    name = fields.Char(string="Name", default="House", required=True)
    active = fields.Boolean(string="Active", default=True, invisible=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="State",
        default="new",
        required=True,
        copy=False,
    )

    def _default_date(self):
        return date.today() + relativedelta(months=3)

    date_availability = fields.Date(
        string="Date Availability", copy=False, default=_default_date
    )
    postcode = fields.Char(string="Postcode")
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    best_price = fields.Float(string="Best Offer", readonly=True)
    description = fields.Text(string="Description")

    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(string="Total Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        string="Garden Orientation",
    )

    property_type_id = fields.Many2one("estate.property.type")
    offer_ids = fields.One2many("estate.offer", "property_id")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("property.tag", )


