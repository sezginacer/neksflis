from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from neksflis.payment.validators import CreditCardNumberValidator


class CreditCardSerializer(serializers.Serializer):
    number = serializers.CharField(validators=[CreditCardNumberValidator()])
    expiry = serializers.DateTimeField(
        input_formats=['%m/%Y', '%Y/%m'],
        validators=[MinValueValidator(timezone.now)]
    )
    security_code = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^[0-9]{3,4}$', message=_('Please enter valid security code.'))])
