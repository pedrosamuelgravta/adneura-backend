from django.urls import path
from api.views.brand_views import BrandView

urlpatterns = [
    path("", BrandView.as_view(), name="brand"),
]
