from django.conf import settings

DEACTIVATE_AFTER_LAST_SUBSCRIPTION = getattr(
    settings, 'DEACTIVATE_AFTER_LAST_SUBSCRIPTION', 3 * 30)  # in days
