# Copyright 2024 Ismail Cagan Yilmaz (https://github.com/milleniumkid)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models, api, fields
from odoo.exceptions import ValidationError


class Website500Errors(models.Model):
    _name = "website.500.errors"
    _description = "Base Model for Website 500 Errors"
    _rec_name = "url"

    url = fields.Char(string="URL")
    request_method = fields.Selection(
        selection=[
            ("GET", "GET"),
            ("POST", "POST"),
            ("PUT", "PUT"),
            ("DELETE", "DELETE"),
            ("HEAD", "HEAD"),
            ("OPTIONS", "OPTIONS"),
            ("PATCH", "PATCH"),
        ],
        string="Request Method",
    )
    form_data = fields.Text(string="Form Data")
    hit_count = fields.Integer(string="Hit Count")
    website_id = fields.Many2one(
        comodel_name="website",
        string="Website",
        ondelete="cascade",
    )

