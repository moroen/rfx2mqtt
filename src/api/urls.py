from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.DefaultRouter()
router.register(r"devices", views.DevicesView)
router.register(r"switches", views.SwitchesView)
router.register(r"lights", views.LightsView)

router.register(r"sensors", views.SensorsView)

router.register(r"temperatures", views.TemperaturesView)

router.register(r"rooms", views.RoomsView)
router.register(r"config", views.ConfigAPIView)


urlpatterns = [
    path("", include(router.urls)),
]
