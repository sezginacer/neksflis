from django.conf import settings

CURRENCY = getattr(settings, 'CURRENCY', 'USD')
