from django.utils.translation import gettext_lazy as _

from neksflis.core.exceptions import BaseProjectException


class SubscriptionPaymentError(BaseProjectException):
    message = _('An error occurred while payment is processing.')
