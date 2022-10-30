from django.urls import path, include
from rest_framework import routers
from m_api import views

router = routers.DefaultRouter()
router.register(r"customer", views.CustomerViewSet)
router.register(r"account", views.AccountViewSet)
router.register(r"card", views.CardViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
