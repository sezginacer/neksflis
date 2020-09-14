import json
import re

import requests
from django.utils.crypto import get_random_string

from neksflis.payment.gateways.base import BaseResponse, BaseGateway


class XyzPaymentGatewayResponse(BaseResponse):
    def is_succeeded(self, response):
        return response.ok

    def get_error_message(self, json_data):
        if self.success:
            return None
        return json_data.get('message', 'Unknown Error.')


class XyzPaymentGatewayTokenResponse(XyzPaymentGatewayResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card_token = self.as_json.get('token')


class XyzPaymentGateway(BaseGateway):
    response_class = XyzPaymentGatewayResponse

    def __init__(self, token_email_regex, charge_email_regex):
        super().__init__(None)
        self.token_email_regex = token_email_regex
        self.charge_email_regex = charge_email_regex

    def charge(self, order_number, amount, currency, card_token, user, **kwargs):
        data = dict(
            order_number=order_number,
            amount=str(amount),
            currency=currency,
            card_token=card_token,
            user_email=user.email
        )
        if re.match(self.charge_email_regex, user.email):
            response_data = dict(
                success=True,
                transaction_id=get_random_string()
            )
            status_code = 200
        else:
            response_data = dict(
                success=False,
                message='an error occurred.',
            )
            status_code = 401
        return self._get_dummy_response(data, response_data, status_code)

    def get_card_token(self, number, expiry, security_code, user, **kwargs):
        data = dict(
            card_number=number,
            card_expiry=expiry.strftime('%Y-%m'),
            card_cvv=security_code,
            user_email=user.email
        )

        if re.match(self.token_email_regex, user.email):
            response_data = dict(
                success=True,
                transaction_id=get_random_string(),
                token=get_random_string()
            )
            status_code = 200
        else:
            response_data = dict(
                success=False,
                message='an error occurred.',
            )
            status_code = 401
        return self._get_dummy_response(
            data, response_data, status_code, XyzPaymentGatewayTokenResponse)

    @staticmethod
    def _get_dummy_response(
            request_data, response_data, status_code, response_class=None):
        response_class = response_class or XyzPaymentGatewayResponse
        request = requests.PreparedRequest()
        request.url = None
        request.body = json.dumps(request_data)
        response = requests.Response()
        response._content = bytes(json.dumps(response_data), encoding='utf-8')
        response.status_code = status_code
        return response_class(request, response)
