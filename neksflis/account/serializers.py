from rest_framework import serializers

from neksflis.account.models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        extra_kwargs = dict(
            first_name=dict(required=True, allow_null=False, allow_blank=False),
            last_name=dict(required=True, allow_null=False, allow_blank=False),
            email=dict(required=True, allow_null=False, allow_blank=False),
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user
