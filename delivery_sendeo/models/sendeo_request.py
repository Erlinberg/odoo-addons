# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import requests
from odoo import _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

SENDEO_API_URL = "https://api.sendeo.com.tr"


class SendeoRequest:
    """Interface between Sendeo Kargo REST API and Odoo recordset
       Abstract Aras Kargo API Operations to connect them with Odoo

       Not all the features are implemented, but could be easily extended with
       the provided API. We leave the operations empty for future.
    """

    def __init__(self, username, password, prod=False):
        """Initialize the API client with the credentials."""
        data = {
            'musteri': username if prod else 'TEST',
            'sifre': password if prod else 'TesT.43e54',
        }
        self.session = requests.Session()
        response = self._process_post_request("/api/Token/LoginAES", data, init=True)
        self.jwt_token = response['Token']

    def _process_post_request(self, url, vals, init=False, post_with_params=False):
        """Sends a POST request to the API and returns the response,
         if any error occurs, raises a ValidationError
         :param url: str
         :param vals: dict
         :returns dict
         """
        headers = {'Content-Type': 'application/json'}
        url = "%s%s" % (SENDEO_API_URL, url)
        if not init:
            headers.update({'Authorization': "Bearer %s" % self.jwt_token})

        if post_with_params:
            response = self.session.post(url, params=vals, headers=headers).json()
        else:
            response = self.session.post(url, json=vals, headers=headers).json()

        if response['StatusCode'] == 200:
            return response['result']
        else:
            raise ValidationError(_("Sendeo API Error.\nError Message: %s" % response['exceptionMessage']))

    def _process_get_request(self, url, vals):
        """Sends a GET request to the API and returns the response,
         if any error occurs, raises a ValidationError
         :param url: str
         :param vals: dict
         :returns dict
         """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer %s" % self.jwt_token
        }
        url = "%s%s" % (SENDEO_API_URL, url)
        response = self.session.get(url, params=vals, headers=headers).json()
        if response['StatusCode'] == 200:
            return response['result']
        else:
            raise ValidationError(_("Sendeo API Error.\nError Message: %s" % response['exceptionMessage']))

    def _set_delivery(self, picking_vals):
        """Create new shipment
        :params vals dict of needed values
        :returns dict with Sendeo response containing the shipping code and label
        """

        response = self._process_post_request(
            url="/api/Cargo/SETDELIVERY",
            vals=picking_vals,
        )
        return response

    def _shipping_label(self, reference_number, barcode_type):
        """Get shipping label for the given ref
        :param reference_number: str
        :param barcode_type: str
        :returns: base64 with pdf labels
        """
        barcode_label_type = "1" if barcode_type == "pdf" else "2"
        vals = {
            'barcodeLabelType': barcode_label_type,
            'referenceNo': reference_number,
        }
        response = self._process_post_request(
            url="/api/Cargo/GETBARCODE",
            vals=vals
        )
        return response

    def _cancel_shipment(self, reference=False):
        """Cancel the expedition for the given ref
        :param str reference -- reference (picking name)
        :param str tracking_number -- tracking number
        :returns: bool True if success
        """
        vals = {
            'referenceNo': reference,
        }
        response = self._process_post_request(
            url="/api/Cargo/CANCELDELIVERY",
            vals=vals,
            post_with_params=True
        )
        return bool(response)

    def _get_tracking_states(self, reference=False):
        """Get tracking status of the given ref
        :param str reference -- reference (picking name)
        :param str tracking_number -- tracking number
        :returns: bool True if success
        """
        vals = {
            'referenceNo': reference,
        }
        response = self._process_get_request(
            url="/api/Cargo/TRACKDELIVERY",
            vals=vals,
        )
        return response
