from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


def luhn_checksum(card_number):
    sum_ = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1

    for i in range(0, num_digits):
        digit = int(card_number[i])

        if not ((i & 1) ^ oddeven):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9

        sum_ = sum_ + digit

    return (sum_ % 10) == 0


class CreditCardNumberValidator:
    def __init__(self, message=None):
        self.message = message or _('Please enter valid credit card number.')
        self.regex_validator = RegexValidator(
            regex=r'^[0-9]{15,16}$',
            message=_('Please enter valid credit card number.')
        )

    def __call__(self, value):
        self.regex_validator(value)
        if not luhn_checksum(value):
            raise ValidationError(self.message)
