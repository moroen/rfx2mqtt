from django.shortcuts import render
from rest_framework import viewsets
from devices.models import Device, Temperature

from devices.serializers import DeviceSerializer, TemperatureSerializer

# Create your views here.


class DevicesAPIView(viewsets.ModelViewSet):
    queryset = Device.objects.all().select_subclasses()
    serializer_class = DeviceSerializer


class TemperatureAPIView(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer
