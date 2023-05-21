from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.forms.models import model_to_dict


from rest_framework import viewsets
from rest_framework.decorators import action

from .serializers import (
    ConfigSerializer,
    DeviceSerializer,
    RoomSerializer,
    LightSerializer,
    SwitchSerializer,
    TemperatureSerializer,
    DevicePolymorphicSerializer,
    SensorPolymorphicSerializer,
)
from .models import Device, Room, Switch, Light, Temperature, Sensor

from constance.backends.database.models import Constance
from constance import config

from json import loads

from rfx2mqtt.log import get_log


log = get_log("api.views")


class RoomsView(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class LightsView(viewsets.ModelViewSet):
    queryset = Light.objects.all()
    serializer_class = LightSerializer


class SwitchesView(viewsets.ModelViewSet):
    queryset = Switch.objects.all()
    serializer_class = SwitchSerializer


class TemperaturesView(viewsets.ModelViewSet):
    queryset = Temperature.objects.all()
    serializer_class = TemperatureSerializer


class SensorsView(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorPolymorphicSerializer


# Create your views here.
class DevicesView(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DevicePolymorphicSerializer
    description = "Devices"

    # def update(self, request: HttpRequest, pk=None):
    #     mdl = self.get_object()

    #     if "state" in request.POST:
    #         mdl.set_state(True)
    #     else:
    #         mdl.set_state(False)

    #     return super().update(request, pk)

    # @action(detail=True, methods=["get"])
    # def on(self, request, pk=None):
    #     return self.set_state(True)

    # @action(detail=True, methods=["get"])
    # def off(self, request, pk=None):
    #     return self.set_state(False)

    # @action(detail=True, methods=["post", "put"])
    # def state(self, request: HttpRequest, pk=None):
    #     reqJson = loads(request.body)
    #     return self.set_state(reqJson["state"])

    # def set_state(self, state):
    #     mdl: Device = self.get_object()
    #     mdl.set_state(state)
    #     mdl.save()
    #     retJson = model_to_dict(mdl)
    #     return JsonResponse(retJson)


class ConfigAPIView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConfigSerializer
    queryset = Constance.objects.all()

    @action(detail=False, methods=["post", "put"])
    def set(self, request: HttpRequest, pk=None):
        dataJson = loads(request.body)
        for k, v in dataJson.items():
            try:
                setattr(config, k, v)
            except AttributeError:
                return JsonResponse({"status": "error", "error": "Unknown config key"})

        return JsonResponse({"status": "ok"})
