from django.shortcuts import render
from rest_framework import viewsets
from devices.models import Device, Temperature
from rooms.models import Room

from devices.serializers import DeviceSerializer, TemperatureSerializer
from rooms.serializers import RoomsSerializer

# Create your views here.


class DevicesAPIView(viewsets.ModelViewSet):
    # queryset = Device.objects.all().select_subclasses()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        qs = Device.objects.all().select_subclasses()
        room = self.request.query_params.get("room")
        if room is not None:
            qs = qs.filter(room=room)

        return qs


class TemperatureAPIView(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class RoomsAPIView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomsSerializer
