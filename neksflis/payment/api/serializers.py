from django_enum_choices.serializers import EnumChoiceField
from rest_framework import serializers

from neksflis.payment.enums import GatewayChoices
from neksflis.payment.models import PaymentOption


class PaymentOptionSerializer(serializers.ModelSerializer):
    gateway = EnumChoiceField(GatewayChoices)

    def validate(self, attrs):
        serializer = attrs['gateway'].config_serializer_class(data=attrs['config'])
        serializer.is_valid()
        if serializer.errors:
            raise serializers.ValidationError(
                dict(config=serializer.errors)
            )
        attrs['config'] = serializer.validated_data
        return attrs

    class Meta:
        model = PaymentOption
        fields = '__all__'
        extra_kwargs = {'config': {'required': True}}
