from django.db.models import Manager
from django.utils import timezone


class SubscriptionManager(Manager):
    def get_active_subscription(self, user):
        try:
            return self.get(
                user=user,
                subscription_period_items__date_range__contains=timezone.now(),
            )
        except self.model.DoesNotExist:
            return None
