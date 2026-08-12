from odoo import fields, models


class PropertyTager(models.Model):
    _name = "property.tag"
    _description = "property.tag"

    name = fields.Char(required=True)
    