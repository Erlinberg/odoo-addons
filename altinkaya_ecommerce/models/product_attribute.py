# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    allow_filling = fields.Boolean(
        string="Allow Filling",
        help="If checked, attribute values will be filled automatically",
        default=True,
    )

    attribute_type = fields.Selection(
        [("attribute", "Attribute"), ("feature", "Feature")],
        string="Attribute Type",
        copy=True,
        default="attribute",
        help="This field is used to distinguish between attributes"
        "and features. Default is attribute.",
    )
