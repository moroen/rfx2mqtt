from rest_framework import routers
from django.urls import path, include
from .views import DevicesAPIView, TemperatureAPIView, RoomsAPIView

app_name = "api"

router = routers.DefaultRouter()

router.register(r"devices", DevicesAPIView, basename="Device")
router.register(r"temperatures", TemperatureAPIView, basename="Temperature")
router.register(r"rooms", RoomsAPIView, basename="Room")

urlpatterns = [path("", include(router.urls))]
