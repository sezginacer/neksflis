from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from neksflis.account.serializers import RegisterSerializer
from neksflis.payment.api.serializers import PaymentOptionSerializer
from neksflis.payment.models import PaymentOption


def clean_database():
    User.objects.all().delete()
    Token.objects.all().delete()
    PaymentOption.objects.all().delete()


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


def register_user():
    data = dict(
        first_name='John',
        last_name='Adams',
        username='john.adams',
        email='john.adams@xyz.com',
        password='password'
    )
    serializer = RegisterSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.create(serializer.validated_data)
    Token.objects.create(user=user)


def run():
    clean_database()
    create_privileged_users()
    create_payment_option()
    register_user()
