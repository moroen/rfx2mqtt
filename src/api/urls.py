from rest_framework import routers
from django.urls import path, include
from .views import DevicesAPIView, TemperatureAPIView

app_name = "api"

router = routers.DefaultRouter()

router.register(r"devices", DevicesAPIView, basename="Device")
router.register(r"temperatures", TemperatureAPIView, basename="Temperature")

urlpatterns = [path("", include(router.urls))]
