from odoo import fields, models, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "estate.property.type"

    _check_unique_name = models.Constraint(
        "UNIQUE(name)",
        "The property type name must be unique.",
    )

    _order = "sequence desc"

    sequence = fields.Integer(defauly=1)


    name = fields.Char(string="Name", required=True)
    property_ids = fields.One2many("real.estate","property_type_id")
