from django.urls import path

from neksflis.account.views import ObtainAuthToken, RegisterView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', ObtainAuthToken.as_view(), name='obtain_token'),
]
