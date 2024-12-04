# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api


class DeliveryPriceRule(models.Model):
    _inherit = "delivery.price.rule"

    variable = fields.Selection(selection_add=[("deci", "Deci")])
    variable_factor = fields.Selection(selection_add=[("deci", "Deci")])
    region_id = fields.Many2one("delivery.region", string="Region", required=True)
    _order = "region_id, sequence, list_price, id"

    @api.onchange("variable")
    def _onchange_variable(self):
        """
        Set `deci` as default value for `variable_factor`
        This field also could have {'readonly': [('variable', '=', 'deci')]}
        """
        if self.variable == "deci":
            self.variable_factor = "deci"
