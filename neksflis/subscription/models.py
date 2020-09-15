from django.conf import settings
from django.contrib.postgres.fields import DateTimeRangeField
from django.db import models
from django.utils import timezone
from django_enum_choices.fields import EnumChoiceField

from neksflis.core.models import StarterModel
from neksflis.subscription.enums import (
    SubscriptionStatus,
    SubscriptionPlan,
    PaymentStatus
)
from neksflis.subscription.managers import SubscriptionManager


class Subscription(StarterModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to=dict(is_staff=False, is_superuser=False),
        related_name='subscriptions'
    )
    payment_option = models.ForeignKey(
        'payment.PaymentOption',
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    status = EnumChoiceField(
        SubscriptionStatus,
        default=SubscriptionStatus.ACTIVE,
        max_length=32
    )
    plan = EnumChoiceField(SubscriptionPlan, max_length=32)
    cancelled_date = models.DateTimeField(null=True, blank=True)
    payment_data = models.JSONField(default=dict)

    objects = SubscriptionManager()

    def get_period_item(self, date=None):
        date = date or timezone.now()
        try:
            return self.subscription_period_items.get(date_range__contains=date)
        except self.DoesNotExist:
            return None

    @property
    def last_use_date(self):
        if self.status == SubscriptionStatus.ACTIVE:
            period_item = self.get_period_item()
        else:
            period_item = self.subscription_period_items.get(
                date_range__contains=self.cancelled_date
            )
        return period_item.date_range.upper


class SubscriptionPeriodItem(StarterModel):
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='subscription_period_items'
    )
    date_range = DateTimeRangeField()
    payment_status = EnumChoiceField(
        PaymentStatus,
        default=PaymentStatus.PENDING,
        max_length=32
    )
