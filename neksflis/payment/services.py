from django.utils.crypto import get_random_string

from neksflis.payment import conf
from neksflis.payment.enums import TransactionType
from neksflis.payment.models import PaymentTransaction


class BasePaymentService:
    def get_card_token(self, **kwargs):
        raise NotImplementedError

    def charge(self, **kwargs):
        raise NotImplementedError


class PaymentService(BasePaymentService):
    def get_card_token(self, payment_option, number, expiry, security_code, user):
        gateway = payment_option.get_gateway()
        response = gateway.get_card_token(
            number=number,
            expiry=expiry,
            security_code=security_code,
            user=user
        )
        PaymentTransaction.objects.create(
            raw_request=response.raw_request,
            raw_response=response.raw_response,
            is_succeeded=response.success,
            transaction_id=response.as_json.get('transaction_id', get_random_string()),
            transaction_type=TransactionType.token,
            payment_option=payment_option,
        )
        return response

    def charge(self, payment_option, card_token, plan, user):
        gateway = payment_option.get_gateway()
        response = gateway.charge(
            order_number=get_random_string(allowed_chars='0123456789'),
            card_token=card_token,
            amount=plan.price,
            currency=conf.CURRENCY,
            user=user
        )
        transaction = PaymentTransaction.objects.create(
            raw_request=response.raw_request,
            raw_response=response.raw_response,
            is_succeeded=response.success,
            transaction_id=response.as_json.get('transaction_id', get_random_string()),
            transaction_type=TransactionType.charge,
            payment_option=payment_option,
        )
        return response, transaction
