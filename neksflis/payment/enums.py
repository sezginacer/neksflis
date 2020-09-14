from enum import Enum

from neksflis.payment.api.validators import (
    AbcConfigSerializer,
    XyzConfigSerializer,
)
from neksflis.payment.gateways.abc import AbcPaymentGateway
from neksflis.payment.gateways.xyz import XyzPaymentGateway


class TransactionType(Enum):
    token = 'token'
    charge = 'charge'


class GatewayChoices(Enum):
    abc = 'abc'
    xyz = 'xyz'

    __gateways__ = {
        abc: AbcPaymentGateway,
        xyz: XyzPaymentGateway
    }
    __serializers__ = {
        abc: AbcConfigSerializer,
        xyz: XyzConfigSerializer
    }

    @property
    def gateway_class(self):
        return self.__gateways__[self.value]

    @property
    def config_serializer_class(self):
        return self.__serializers__[self.value]
