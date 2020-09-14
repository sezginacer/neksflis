from django.urls import path

from neksflis.content.views import (
    GoldPlanContentView,
    SilverPlanContentView,
    PlatinumPlanContentView
)

urlpatterns = [
    path('silver/', SilverPlanContentView.as_view(), name='silver_plan_content'),
    path('gold/', GoldPlanContentView.as_view(), name='gold_plan_content'),
    path('platinum/', PlatinumPlanContentView.as_view(), name='platinum_plan_content'),
]
