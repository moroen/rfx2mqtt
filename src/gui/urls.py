from django.urls import path
from django.views.generic.base import TemplateView

from .views import TestView, DeviceView, AddView, EditView

urlpatterns = [
    # path("test", TemplateView.as_view(template_name="testing.html"))
    path("test/", TestView.as_view()),
    path("devices/", DeviceView.as_view(), name="devices-view"),
    path("devices/add/", AddView.as_view(), name="device-add-view"),
    path("devices/detail/<pk>", EditView.as_view(), name="device-edit-view"),
]
