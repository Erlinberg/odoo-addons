# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, _, fields, api
from odoo.exceptions import ValidationError


class StockLocation(models.Model):
    _inherit = "stock.location"

    vertical_lift_kardex_id = fields.Many2one(
        "stock.vertical.lift.kardex", string="Vertical Lift Kardex"
    )

    @api.one
    def get_kardex_rack(self):
        if self.vertical_lift_kardex_id:
            self.vertical_lift_kardex_id._get_product(self)
        else:
            raise ValidationError(
                _("No Kardex Vertical Lift Controller is defined for this location.")
            )
        return True
