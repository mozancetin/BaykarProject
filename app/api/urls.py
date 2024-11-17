from django.urls import path, re_path
from rest_framework import permissions
from .views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger API Dökümantasyonu için gerekli fonksiyonu hazırlıyoruz.
schema_view = get_schema_view(
    openapi.Info(
        title="Baykar Hava Aracı Üretim Uygulaması API",
        default_version="v1",
        description="Hava Aracı Üretim Uygulaması projesinin API dökümantasyonu. Authorization için Session kullanıldı. Bu yüzden bu dökümantasyondaki endpointleri denemeden önce bir personel oluşturmanız gerekir.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# /api/v1/ altındaki url pattern'larımızı backendimize ekliyoruz.
urlpatterns = [
    path("employee/list/", list_employees, name="list_employees"),
    path("plane/list/", list_planes, name="list_planes"),
    path("part/list/", list_parts, name="list_parts"),
    path("employee/<int:id>/", get_employee_by_id, name="get_employee_by_id"),
    path("plane/<int:id>/", get_plane_by_id, name="get_plane_by_id"),
    path("part/<int:id>/", get_part_by_id, name="get_part_by_id"),
    path("employee/by-team/", get_employees_by_team, name="get_employees_by_team"),
    path("part/grouped/", get_grouped_parts, name="get_grouped_parts"),
    path("plane/create/", create_plane, name="create_plane"),
    path("part/create/", create_part, name="create_part"),
    path("part/delete/", delete_part, name="delete_part"),
    path("generate/part/<int:count>/", generate_part, name="generate_part"),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

