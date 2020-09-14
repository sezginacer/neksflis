from decimal import Decimal
from enum import Enum


class SubscriptionStatus(Enum):
    ACTIVE = 'active'
    CANCELLED = 'cancelled'


class PaymentStatus(Enum):
    PENDING = 'pending'
    COMPLETED = 'completed'


class SubscriptionPlan(Enum):
    silver = 'silver'
    gold = 'gold'
    platinum = 'platinum'

    __prices__ = {
        silver: Decimal('17.09'),
        gold: Decimal('26.90'),
        platinum: Decimal('39.90')
    }
    __weights__ = {
        silver: 1,
        gold: 2,
        platinum: 3
    }

    def __gt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return self.weight > other.weight

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return self.weight < other.weight

    def __ge__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return self.weight >= other.weight

    def __le__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError
        return self.weight <= other.weight

    @property
    def weight(self):
        return self.__weights__[self.value]

    @property
    def price(self):
        return self.__prices__[self.value]
