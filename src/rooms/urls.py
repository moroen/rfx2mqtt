from django.urls import path
from django.views.generic import TemplateView

from .views import RoomList, RoomAddView, RoomDetailView

app_name = "rooms"

urlpatterns = [
    path("", RoomList.as_view(), name="list"),
    path("add", RoomAddView.as_view(), name="add"),
    path("detail/<pk>", RoomDetailView.as_view(), name="detail"),
    # path("delete/<pk>", DeviceDeleteView.as_view(), name="device-delete"),
]
