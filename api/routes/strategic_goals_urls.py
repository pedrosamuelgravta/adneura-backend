from django.urls import path, include
from api.views.strategic_goals_views import StrategicGoalsView

urlpatterns = [
    path("", StrategicGoalsView.as_view({"get": "list", "post": "create"})),
    path(
        "<uuid:pk>/",
        StrategicGoalsView.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
