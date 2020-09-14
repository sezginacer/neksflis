from django.conf import settings

SUBSCRIPTION_DURATION = getattr(settings, 'SUBSCRIPTION_DURATION', 30)  # in days
SUBSCRIPTION_TRY_CHARGE_DAYS = getattr(settings, 'SUBSCRIPTION_TRY_CHARGE_DAYS', 5)
SUBSCRIPTION_NEW_PERIOD_ITEM_BUFFER = getattr(
    settings, 'SUBSCRIPTION_NEW_PERIOD_ITEM_BUFFER', 3)  # in hours
