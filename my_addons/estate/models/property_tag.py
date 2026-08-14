from odoo import fields, models


class PropertyTager(models.Model):
    _name = "property.tag"
    _description = "property.tag"

    _check_unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property tag name must be unique.",
    )

    _order = "name desc"
    
    name = fields.Char(required=True)
    color = fields.Integer()
