from rest_framework import serializers

from neksflis.subscription.models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    last_use_date = serializers.DateTimeField(read_only=True)

    class Meta:
        exclude = ('payment_data',)
        model = Subscription
