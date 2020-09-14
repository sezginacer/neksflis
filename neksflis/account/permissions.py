from rest_framework.permissions import BasePermission


class SubscriptionPlanPermission(BasePermission):
    def has_permission(self, request, view):
        if request.subscription and view.allowed_plan:
            return request.subscription.plan >= view.allowed_plan
        return False
