from datetime import timedelta

from django.db.models import Q, OuterRef, Exists
from django.utils import timezone
from psycopg2.extras import DateTimeTZRange

from neksflis.celery import app
from neksflis.payment.services import PaymentService
from neksflis.subscription import conf
from neksflis.subscription.enums import PaymentStatus, SubscriptionStatus
from neksflis.subscription.models import Subscription, SubscriptionPeriodItem
from neksflis.subscription.services import SubscriptionService


@app.task
def charge_subscription(subscription_id):
    subscription = Subscription.objects.get(pk=subscription_id)
    payment_service = PaymentService()
    response, transaction = payment_service.charge(
        payment_option=subscription.payment_option,
        card_token=subscription.payment_data.get('token'),
        plan=subscription.plan,
        user=subscription.user
    )
    if response.success:
        period_item = subscription.get_period_item()
        period_item.payment_status = PaymentStatus.COMPLETED
        period_item.save(update_fields=['payment_status', 'updated_date'])

        transaction.subscription_period_item = period_item
        transaction.save(update_fields=['subscription_period_item', 'updated_date'])


@app.task
def charge_subscriptions():
    query = SubscriptionPeriodItem.objects.filter(
        date_range__contains=timezone.now(),
        payment_status=PaymentStatus.PENDING,
        subscription_id=OuterRef('pk')
    )
    subscriptions = Subscription.objects.annotate(
        payment_pending=Exists(query.only('pk'))).filter(
        payment_pending=True, status=SubscriptionStatus.ACTIVE
    )
    for subscription in subscriptions:
        charge_subscription.apply_async(args=(subscription.pk,))


@app.task
def create_new_period_items():
    buffer = conf.SUBSCRIPTION_NEW_PERIOD_ITEM_BUFFER
    next_date = timezone.now() + timedelta(hours=buffer)
    subscriptions = Subscription.objects.filter(
        ~Q(subscription_period_items__date_range__contains=next_date),
        status=SubscriptionStatus.ACTIVE
    )
    subscription_period_items = []
    for subscription in subscriptions:
        date_range = subscription.get_period_item().date_range
        subscription_period_items.append(
            SubscriptionPeriodItem(
                subscription=subscription,
                date_range=DateTimeTZRange(
                    date_range.upper,
                    date_range.upper + timedelta(days=conf.SUBSCRIPTION_DURATION)
                ),
                payment_status=PaymentStatus.PENDING
            )
        )
    SubscriptionPeriodItem.objects.bulk_create(subscription_period_items)


@app.task
def cancel_unpaid_subscriptions():
    service = SubscriptionService()
    gap = conf.SUBSCRIPTION_TRY_CHARGE_DAYS
    query = SubscriptionPeriodItem.objects.filter(
        ~Q(date_range__contains=timezone.now() - timedelta(days=gap)),
        date_range__contains=timezone.now(),
        payment_status=PaymentStatus.PENDING,
        subscription_id=OuterRef('pk')
    )
    subscriptions = Subscription.objects.annotate(
        payment_pending=Exists(query.only('pk'))).filter(payment_pending=True)
    for subscription in subscriptions:
        service.cancel_subscription(subscription)
