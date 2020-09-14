from django.urls import path

from neksflis.subscription.views import SubscriptionViewSet

urlpatterns = [
    path(
        'subscribe/',
        SubscriptionViewSet.as_view({'post': 'subscribe'}),
        name='subscribe'
    ),
    path(
        'unsubscribe/',
        SubscriptionViewSet.as_view({'post': 'unsubscribe'}),
        name='subscribe'
    ),
    path(
        'ongoing/',
        SubscriptionViewSet.as_view({'get': 'ongoing'}),
        name='ongoing'
    ),
]
