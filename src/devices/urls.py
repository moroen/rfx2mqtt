from django.urls import path
from django.views.generic import TemplateView

from .views import DeviceList, DetailView, DeviceDeleteView, DeviceAddView

urlpatterns = [
    path("", DeviceList.as_view(), name="device-list"),
    path("add", DeviceAddView.as_view(), name="device-add"),
    path("detail/<pk>", DetailView.as_view(), name="device-detail"),
    path("delete/<pk>", DeviceDeleteView.as_view(), name="device-delete"),
]
