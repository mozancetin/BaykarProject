from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import register, dashboard, custom_login, custom_logout, team

# / altındaki url pattern'larımızı backendimize ekliyoruz.
urlpatterns = [
    path("", custom_login, name="login"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/team/", team, name="team"),
    path('register/', register, name='register'),
    path('logout/', custom_logout, name='logout')
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)