from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from neksflis.subscription.services import SubscriptionService


class SubscriptionMiddleware(MiddlewareMixin):
    service = SubscriptionService()

    def process_request(self, request):
        def get_subscription():
            if request.user and request.user.pk:
                return self.service.get_active_subscription(request.user)
            return None
        request.subscription = SimpleLazyObject(get_subscription)
