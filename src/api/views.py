from django.shortcuts import render
from rest_framework import viewsets
from devices.models import Device

from .serializers import DeviceSerializer

# Create your views here.


class DevicesAPIView(viewsets.ModelViewSet):
    queryset = Device.objects.all().select_subclasses()
    serializer_class = DeviceSerializer
