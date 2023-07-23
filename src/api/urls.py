from rest_framework import routers
from django.urls import path, include
from .views import DevicesAPIView

app_name = "api"

router = routers.DefaultRouter()

router.register(r"devices", DevicesAPIView, basename="Device")

urlpatterns = [path("", include(router.urls))]
