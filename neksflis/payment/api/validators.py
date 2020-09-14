from rest_framework import serializers


class AbcConfigSerializer(serializers.Serializer):
    url = serializers.URLField()
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=64)
    secret_key = serializers.CharField(max_length=64)


class XyzConfigSerializer(serializers.Serializer):
    token_email_regex = serializers.CharField()
    charge_email_regex = serializers.CharField()
