from typing import Any
from django.db import models
from model_utils.managers import InheritanceManager
import decimal

from django.urls import reverse

# Create your models here.

from rooms.models import Room
from django_rfx.models import PacketType, Protocol

import logging

import django_rfx as rfx

log = logging.getLogger("devices")


class Device(models.Model):
    objects = InheritanceManager()

    name = models.CharField(max_length=200, default="New device")
    ident = models.CharField(max_length=20, default="0123456")
    unit = models.CharField(max_length=10, default="1")

    device_protocol = models.ForeignKey(
        Protocol, on_delete=models.CASCADE, null=True, blank=True
    )
    packet_type = models.ForeignKey(
        PacketType, on_delete=models.CASCADE, default="0x03"
    )

    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    room = models.ForeignKey(
        Room, related_name="devices", on_delete=models.CASCADE, default=1
    )

    def get_absolute_url(self):
        return reverse("device-detail", kwargs={"pk": self.id})

    def set_state(self, state: bool = None, brightness: int = None) -> bool:
        log.debug(
            "Setting state to {} for device {}:{} with packet_type {}".format(
                state, self.ident, self.unit, self.packet_type_id
            )
        )
        rfx.set_state(
            "{}:{}".format(self.ident, self.unit),
            self.packet_type_id,
            state,
        )


class Switch(Device):
    state = models.BooleanField(default=False)


class Light(Device):
    state = models.BooleanField(default=False)
    brightness = models.IntegerField(default=50)


class Sensor(Device):
    pass


class Temperature(Sensor):
    temp = models.fields.DecimalField(
        max_digits=5, decimal_places=1, default=decimal.Decimal(20.0)
    )
    humidity = models.fields.IntegerField(null=True, blank=True)
