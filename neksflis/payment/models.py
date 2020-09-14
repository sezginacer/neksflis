from django.db import models
from django_enum_choices.fields import EnumChoiceField

from neksflis.core.models import StarterModel
from neksflis.payment.enums import GatewayChoices, TransactionType


class PaymentOption(StarterModel):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=16, unique=True)
    gateway = EnumChoiceField(GatewayChoices, max_length=32)
    is_active = models.BooleanField(default=True)
    config = models.JSONField(default=dict)

    def get_gateway(self):
        return self.gateway.gateway_class(**self.config)

    def __str__(self):
        return f'{self.name}'


class PaymentTransaction(StarterModel):
    transaction_id = models.CharField(max_length=128)
    raw_request = models.TextField()
    raw_response = models.TextField()
    is_succeeded = models.BooleanField()
    payment_option = models.ForeignKey(
        PaymentOption,
        on_delete=models.PROTECT,
        related_name='payment_transactions'
    )
    transaction_type = EnumChoiceField(TransactionType, max_length=32)
    subscription_period_item = models.ForeignKey(
        'subscription.SubscriptionPeriodItem',
        null=True,
        on_delete=models.PROTECT,
        related_name='payment_transactions',
    )

    class Meta:
        unique_together = [['transaction_id', 'payment_option']]
