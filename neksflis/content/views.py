from rest_framework.response import Response
from rest_framework.views import APIView

from neksflis.content.mixins import SubscriptionRequiredMixin
from neksflis.subscription.enums import SubscriptionPlan


class SubscriptionPlanContentView(SubscriptionRequiredMixin, APIView):
    def get(self, request, *args, **kwargs):
        return Response({'message': f'Here is {self.allowed_plan.value} plan content!'})


class SilverPlanContentView(SubscriptionPlanContentView):
    allowed_plan = SubscriptionPlan.silver


class GoldPlanContentView(SubscriptionPlanContentView):
    allowed_plan = SubscriptionPlan.gold


class PlatinumPlanContentView(SubscriptionPlanContentView):
    allowed_plan = SubscriptionPlan.platinum
