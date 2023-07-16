from django.urls import path
from django.views.generic import TemplateView

from .views import DeviceList, DetailView

urlpatterns = [
    path("", DeviceList.as_view(), name="device-list"),
    path("detail/<pk>", DetailView.as_view(), name="device-detail"),
]
