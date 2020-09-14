from datetime import timedelta

from django.db.transaction import atomic
from django.utils import timezone
from psycopg2.extras import DateTimeTZRange

from neksflis.payment.services import PaymentService
from neksflis.subscription import conf, exceptions
from neksflis.subscription.enums import SubscriptionStatus, PaymentStatus
from neksflis.subscription.models import Subscription, SubscriptionPeriodItem


class SubscriptionService:
    payment_service = PaymentService()

    def create_subscription(self, plan, user, credit_card, payment_option):
        response = self.payment_service.get_card_token(
            payment_option=payment_option, user=user, **credit_card)
        if not response.success:
            raise exceptions.SubscriptionPaymentError()

        response, transaction = self.payment_service.charge(
            payment_option=payment_option,
            card_token=response.card_token,
            plan=plan,
            user=user
        )
        if not response.success:
            raise exceptions.SubscriptionPaymentError()

        with atomic():
            subscription = Subscription.objects.create(
                user=user,
                plan=plan,
                payment_option=payment_option,
                status=SubscriptionStatus.ACTIVE,
                payment_data=dict(card_token=response.card_token)
            )

            start_date, end_date = self._get_start_and_end_dates()
            subscription_period_item = SubscriptionPeriodItem.objects.create(
                subscription=subscription,
                payment_status=PaymentStatus.COMPLETED,
                date_range=DateTimeTZRange(start_date, end_date)
            )

            transaction.subscription_period_item = subscription_period_item
            transaction.save(update_fields=['updated_date', 'subscription_period_item'])
        return subscription

    @atomic()
    def cancel_subscription(self, subscription):
        now = timezone.now()
        subscription_period_item = subscription.get_period_item()
        if subscription_period_item.payment_status == PaymentStatus.PENDING:
            subscription_period_item.date_range = DateTimeTZRange(
                subscription_period_item.date_range.lower, now
            )
            subscription_period_item.save(update_fields=['date_range', 'updated_date'])

        pending_item = subscription.subscription_period_items.filter(
            created_date__gt=subscription_period_item.created_date).first()
        if pending_item:  # if next subscription period item created, fix it too.
            pending_item.date_range = DateTimeTZRange(
                subscription_period_item.date_range.upper,
                subscription_period_item.date_range.upper + timedelta(microseconds=1)
            )
            pending_item.save(update_fields=['date_range', 'updated_date'])

        subscription.status = SubscriptionStatus.CANCELLED
        subscription.cancelled_date = now
        subscription.save(update_fields=['status', 'cancelled_date', 'updated_date'])

    def get_active_subscription(self, user):
        return Subscription.objects.get_active_subscription(user)

    @staticmethod
    def _get_start_and_end_dates():
        start_date = timezone.now()
        end_date = start_date + timedelta(days=conf.SUBSCRIPTION_DURATION)
        return start_date, end_date
