from neksflis.account.permissions import SubscriptionPlanPermission


class SubscriptionRequiredMixin:
    permission_classes = [SubscriptionPlanPermission]
    allowed_plan = None
