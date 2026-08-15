from odoo import _, api, fields, models


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
    property_ids = fields.One2many("real.estate", "property_type_id")
    property_count = fields.Integer(compute="_compute_property_count")

    offer_ids = fields.One2many("estate.offer", "property_type_id", string="Offers")

    offer_count = fields.Integer(string="Offers Count", compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    @api.depends("property_ids")
    def _compute_property_count(self):
        for rec in self:
            rec.property_count = len(rec.property_ids)

    def action_open_property_ids(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "estate.real_estate_action"
        )
        action["domain"] = [("property_type_id", "=", self.id)]
        action["context"] = {"default_property_type_id": self.id}
        return action
