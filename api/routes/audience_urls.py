from django.urls import path
from api.views.audience_views import (
    AudienceListView,
    AudienceUpdateView,
)
from api.views.territory_views import (
    TerritoriesView,
)
from api.views.trigger_view import (
    TriggerView,
    TriggerUpdateView,
)
from api.views.generate_image_views import (
    GenerateImageTriggerView,
    GenerateImageAudienceView,
)

urlpatterns = [
    path("", AudienceListView.as_view(), name="audiences"),
    path("<int:pk>/", AudienceUpdateView.as_view(), name="audience"),
    path("trigger/", TriggerView.as_view(), name="trigger"),
    path("trigger/<int:pk>/", TriggerUpdateView.as_view(), name="trigger"),
    path("territories/", TerritoriesView.as_view(), name="territories"),
    path(
        "generate-image-audience/",
        GenerateImageAudienceView.as_view(),
        name="generate-image-audience",
    ),
    path(
        "generate-image-trigger/",
        GenerateImageTriggerView.as_view(),
        name="generate-image-trigger",
    ),
]
