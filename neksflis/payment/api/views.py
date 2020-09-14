from rest_framework import viewsets, permissions, authentication

from neksflis.payment.api.serializers import PaymentOptionSerializer
from neksflis.payment.models import PaymentOption


class PaymentOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [authentication.TokenAuthentication]
    queryset = PaymentOption.objects.all()
    serializer_class = PaymentOptionSerializer
