from django.utils.crypto import get_random_string

from neksflis.payment.gateways.base import BaseResponse, BaseGateway


class AbcPaymentGatewayResponse(BaseResponse):
    def is_succeeded(self, response):
        return response.ok

    def get_error_message(self, json_data):
        if self.success:
            return None
        return json_data.get('error_message', 'Unknown Error.')

    def normalize_response(self, json_data):
        json_data.setdefault('transaction_id', get_random_string())
        return json_data


class AbcPaymentGatewayTokenResponse(AbcPaymentGatewayResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card_token = self.as_json.get('card_token')


class AbcPaymentGateway(BaseGateway):
    response_class = AbcPaymentGatewayResponse

    def __init__(self, url, username, password, secret_key):
        super().__init__(url)
        self.username = username
        self.password = password
        self.secret_key = secret_key

    def get_auth(self):
        return self.username, self.password

    def get_headers(self):
        return {'X-Secret-Key': self.secret_key}

    def charge(self, order_number, amount, currency, card_token, user, **kwargs):
        data = dict(
            order_number=order_number,
            amount=str(amount),
            currency=currency,
            card_token=card_token,
            user_email=user.email,
        )
        response = self.send_request(
            'POST',
            data=data,
            url=self._get_url(action='charge')
        )
        return response

    def get_card_token(self, number, expiry, security_code, user, **kwargs):
        expiry_year, expiry_month = self._get_expiry_year_month(expiry)
        data = dict(
            card_number=number,
            card_year=expiry_year,
            card_month=expiry_month,
            card_cvv=security_code,
            user_email=user.email
        )
        response = self.send_request(
            'POST',
            data=data,
            url=self._get_url(action='token'),
            response_class=AbcPaymentGatewayTokenResponse
        )
        return response

    def _get_url(self, action=None):
        if action is None:
            return self.url
        url = self.url.rstrip('/')
        return f'{url}/{action}/'

    @staticmethod
    def _get_expiry_year_month(card_expiry):
        return card_expiry.year, card_expiry.month
