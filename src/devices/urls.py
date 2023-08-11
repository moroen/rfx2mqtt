from django.urls import path
from django.views.generic import TemplateView

from .views import DeviceList, DetailView, DeviceDeleteView, DeviceAddView

app_name = "devices"

urlpatterns = [
    path("", DeviceList.as_view(), name="list"),
    path("add", DeviceAddView.as_view(), name="add"),
    path("detail/<pk>", DetailView.as_view(), name="detail"),
    path("delete/<pk>", DeviceDeleteView.as_view(), name="delete"),
]
