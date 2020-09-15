from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from neksflis.account import conf
from neksflis.celery import app


@app.task
def deactivate_unsubscribed_users():
    buffer_days = conf.DEACTIVATE_AFTER_LAST_SUBSCRIPTION
    now = timezone.now()
    day = now - timedelta(days=buffer_days)
    users = get_user_model().objects.exclude(
        subscriptions__subscription_period_items__date_range__contains=day)
    users.update(is_active=False)
