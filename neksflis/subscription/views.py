from django.http import Http404
from rest_framework import permissions, authentication, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from neksflis.core.mixins import MultiSerializerViewSetMixin
from neksflis.subscription.serializers import (
    SubscribeSerializer,
    SubscriptionDetailSerializer,
    UnsubscribeSerializer
)
from neksflis.subscription.services import SubscriptionService


class SubscriptionViewSet(MultiSerializerViewSetMixin,
                          GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    serializer_class = SubscriptionDetailSerializer
    service = SubscriptionService()

    serializers = dict(
        subscribe=SubscribeSerializer,
        ongoing=SubscriptionDetailSerializer,
        unsubscribe=UnsubscribeSerializer
    )

    def subscribe(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        self.service.create_subscription(**serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def ongoing(self, request, *args, **kwargs):
        subscription = self._get_active_subscription()
        serializer_class = self.get_serializer_class()
        return Response(serializer_class(subscription).data)

    def unsubscribe(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        subscription = self._get_active_subscription()
        self.service.cancel_subscription(subscription)
        return Response(self.serializer_class(subscription).data)

    def _get_active_subscription(self):
        subscription = self.service.get_active_subscription(self.request.user)
        if subscription is None:
            raise Http404
        return subscription
