from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class BaseProjectException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = _('A server error occurred.')

    def __init__(self, params=None):
        self.detail = self.message % (params or {})
