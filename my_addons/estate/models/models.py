from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class RealEstate(models.Model):
    _name = "real.estate"
    _description = "estate.estate"

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive.",
    )
    _check_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)",
        "The selling price must be positive.",
    )

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
    best_price = fields.Float(
        string="Best Offer", readonly=True, compute="_compute_best_price"
    )

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):
                min_price = record.expected_price * 0.90

                if (
                    float_compare(
                        record.selling_price, min_price, precision_rounding=0.01
                    )
                    < 0
                ):
                    raise ValidationError(
                        _(
                            "The selling price cannot be lower than 90% of the expected price!"
                        )
                    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            offers = rec.offer_ids.mapped("price")
            rec.best_price = max(offers) if offers else 0.0

    description = fields.Text(string="Description")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(
        string="Total Area (sqm)", compute="_compute_total_area"
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

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
    tag_ids = fields.Many2many("property.tag")
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
    )

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.onchange("date_availability")
    def _onchange_date_availability(self):
        if self.date_availability and self.date_availability < fields.Date.today():
            return {
                "warning": {
                    "title": _("Warning"),
                    "message": _("The availability date cannot be set in the past."),
                }
            }

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(_("Canceled properties cannot be set as sold."))
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("Sold properties cannot be canceled."))
            record.state = "canceled"
        return True
