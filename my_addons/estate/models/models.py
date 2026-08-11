from odoo import models, fields, api


class RealEstate(models.Model):
    _name = "real.estate"
    _description = "estate.estate"

    name = fields.Char(default="House", required=True)
    price = fields.Float()


#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
