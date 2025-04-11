from django.urls import path
from api.views.audience_views import AudienceListView, TriggerView, GenerateImageAudienceView, GenerateImageTriggerView

urlpatterns = [
    path('', AudienceListView.as_view(), name='audiences'),
    path('trigger/', TriggerView.as_view(), name='trigger'),
    path('generate-image-audience/', GenerateImageAudienceView.as_view(), name='generate-image-audience'),
    path('generate-image-trigger/', GenerateImageTriggerView.as_view(), name='generate-image-trigger'),
]