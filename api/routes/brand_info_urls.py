from django.urls import path
from api.views.brand_info_views import BrandInfoView

urlpatterns = [
    path('', BrandInfoView.as_view(), name='brand'),
]