from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.routes.auth_urls")),
    path("brands/", include("api.routes.brand_urls")),
    path("brand-info/", include("api.routes.brand_info_urls")),
    path("audiences/", include("api.routes.audience_urls")),
    path("strategic-goals/", include("api.routes.strategic_goals_urls")),
]
