from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("messaging/", include("m_messaging.urls")),
    path("api/", include("m_api.urls")),
]
