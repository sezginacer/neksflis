from django.utils.translation import gettext_lazy as _
from django_enum_choices.serializers import EnumChoiceField
from rest_framework import serializers

from neksflis.payment.models import PaymentOption
from neksflis.payment.serializers import CreditCardSerializer
from neksflis.subscription.enums import SubscriptionPlan, SubscriptionStatus
from neksflis.subscription.services import SubscriptionService


class SubscribeSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    payment_option = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=PaymentOption.objects.filter(is_active=True)
    )
    plan = EnumChoiceField(enum_class=SubscriptionPlan)
    credit_card = CreditCardSerializer()

    def validate(self, attrs):
        service = SubscriptionService()
        subscription = service.get_active_subscription(attrs['user'])
        if subscription:
            raise serializers.ValidationError(
                _('You have already an active subscription.'))
        return attrs


class SubscriptionDetailSerializer(serializers.Serializer):
    payment_option = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=PaymentOption.objects.filter(is_active=True)
    )
    plan = EnumChoiceField(enum_class=SubscriptionPlan)
    status = EnumChoiceField(enum_class=SubscriptionStatus)
    last_use_date = serializers.DateTimeField(read_only=True)


class UnsubscribeSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=512)
