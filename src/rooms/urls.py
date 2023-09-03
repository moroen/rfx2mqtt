from django.urls import path
from django.views.generic import TemplateView

from .views import RoomListView, RoomAddView, RoomDetailView

app_name = "rooms"

urlpatterns = [
    path("", RoomListView.as_view(), name="list"),
    # path("test", TestView.as_view(), name="test"),
    path("add", RoomAddView.as_view(), name="add"),
    path("detail/<pk>", RoomDetailView.as_view(), name="detail"),
    # path("delete/<pk>", DeviceDeleteView.as_view(), name="device-delete"),
]
