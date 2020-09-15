from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

from neksflis.payment.api.serializers import PaymentOptionSerializer
from neksflis.payment.models import PaymentOption, PaymentTransaction
from neksflis.subscription.models import SubscriptionPeriodItem, Subscription

User = get_user_model()


def clean_database():
    models = [
        PaymentTransaction, SubscriptionPeriodItem,
        Subscription, PaymentOption, Token, User,
    ]
    for model in models:
        model.objects.all().delete()


def create_privileged_users():
    User.objects.create_superuser('admin', 'admin@admin.com', 'admin')


def create_payment_option():
    serializer = PaymentOptionSerializer(data=dict(
            name='XYZ Pay',
            slug='xyz',
            gateway='xyz',
            config=dict(
                token_email_regex='.*@xyz.com',
                charge_email_regex='.*@xyz.com',
            )
        )
    )
    assert serializer.is_valid()
    serializer.create(serializer.validated_data)


def run():
    clean_database()
    create_privileged_users()
    create_payment_option()
