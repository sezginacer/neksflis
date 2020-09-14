from rest_framework import renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken as DrfObtainAuthToken
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView

from neksflis.account.serializers import RegisterSerializer


class ObtainAuthToken(DrfObtainAuthToken):
    throttle_classes = (UserRateThrottle,)
    throttle_scope = 'obtain_token'


class RegisterView(APIView):
    throttle_classes = (UserRateThrottle,)
    permission_classes = ()
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = RegisterSerializer
    throttle_scope = 'register'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.create(serializer.validated_data)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
