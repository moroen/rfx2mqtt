from typing import Any
from django.db import models
from django.utils.html import format_html
from model_utils.managers import InheritanceManager
from django.template.loader import render_to_string
from django.core.serializers.json import DjangoJSONEncoder
from json import dumps
import decimal

from django.urls import reverse, reverse_lazy

# Create your models here.

from rooms.models import Room
from django_rfx.models import PacketType, Protocol
import logging

from constance import config

# Transports
import django_rfx as rfx
import django_mqtt as mqtt

log = logging.getLogger("devices")


class Device(models.Model):
    objects = InheritanceManager()

    name = models.CharField(max_length=200, default="New device")
    ident = models.CharField(max_length=20, default="0123456")
    unit = models.CharField(max_length=10, default="1")

    mqtt_discover = models.BooleanField(default=True)

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

    mqtt_topic_type = "device"

    def get_absolute_url(self):
        return reverse("DEVICES:detail", kwargs={"pk": self.id})

    def set_state(self, state: bool = None, brightness: int = None) -> bool:
        state = self.state if state is None else state

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

        if hasattr(self, "brightness"):
            brightness = self.brightness if brightness is None else brightness
            rfx.set_level(
                "{}:{}".format(self.ident, self.unit), self.packet_type_id, brightness
            )

    def render_widget(self):
        return format_html(f"<div>Widget</div>")

    def mqtt_get_state_topic(self) -> str:
        return "{}/{}/{}/state".format(config.MQTT_TOPIC, self.mqtt_topic_type, self.id)

    def mqtt_get_command_topic(self) -> str:
        return "{}/{}/{}/set".format(config.MQTT_TOPIC, self.mqtt_topic_type, self.id)

    def mqtt_send_state(self, stateObj=None):
        if stateObj is not None:
            topic = self.mqtt_get_state_topic()
            payload = dumps(stateObj, cls=DjangoJSONEncoder)
            mqtt.publish(topic, payload, retain=True)
        else:
            log.error("send_state stateObj empty")

    def mqtt_send_config_object(self, sub_config=None, config_type=None):
        log.debug("Send config object for device {}".format(self.id))
        cObj = {
            "command_topic": self.mqtt_get_command_topic(),
            "state_topic": self.mqtt_get_state_topic(),
            "name": "{} - {}".format(self.room, self.name)
            if config.MQTT_ROOM_IN_NAME
            else self.name,
            "unique_id": "rfx_{}_{}".format(self.ident, self.unit),
        }

        if sub_config is not None:
            cObj.update(sub_config)

        cType = config_type.lower() if config_type is not None else self.mqtt_topic_type

        payload = dumps(cObj)
        topic = "{}/{}/{}/config".format(config.MQTT_TOPIC, cType, self.id)

        mqtt.publish(topic, payload, retain=True)


class Switch(Device):
    state = models.BooleanField(default=False)
    mqtt_topic_type = "switch"

    def mqtt_send_state(self, stateObj=None):
        stateObj = {"state": self.state}
        return super().mqtt_send_state(stateObj)

    def render_widget(self):
        return render_to_string(
            "widgets/hx_switch.html",
            context={
                "id": self.id,
                "state": self.state,
                "target": reverse_lazy("API:Device-detail", kwargs={"pk": self.id}),
            },
        )

    def mqtt_send_config_object(self):
        cObj = {
            "availability": [{"topic": "zigbee2mqtt/bridge/state"}],
            "json_attributes_topic": "{}/{}/set".format(config.MQTT_TOPIC, self.id),
            "payload_off": '{"state": false}',
            "payload_on": '{"state": true}',
            # "value_template": '{{ value_json.state }}'
        }

        # print(self.__class__.__name__)

        return super().mqtt_send_config_object(cObj)


class Light(Device):
    state = models.BooleanField(default=False)
    brightness = models.IntegerField(default=50)
    mqtt_topic_type = "light"

    def mqtt_send_config_object(self):
        cObj = {
            "brightness": True,
            "brightness_scale": 100,
            "payload_off": False,
            "payload_on": True,
            # "value_template": '{{ value_json.state }}'
        }
        return super().mqtt_send_config_object(cObj)


class Sensor(Device):
    def set_state(self, state: bool = None, brightness: int = None) -> bool:
        log.debug("Sensors does not do states")


class Temperature(Sensor):
    temp = models.fields.DecimalField(
        max_digits=5, decimal_places=1, default=decimal.Decimal(20.0)
    )
    humidity = models.fields.IntegerField(null=True, blank=True)

    mqtt_topic_type = "sensor"

    def render_widget(self):
        return render_to_string(
            "widgets/temp_hum.html",
            context={"temperature": self.temp, "humidity": self.humidity},
        )

    def mqtt_send_state(self):
        sObj = {"temperature": self.temp, "humidity": self.humidity}
        super().mqtt_send_state(sObj)

    def mqtt_send_config_object(self):
        cObj = {
            "device_class": "temperature",
            # "name": "Temperature",
            # "state_topic": "rfx2mqtt/{}".format(self.id),
            "unit_of_measurement": "C",
            "value_template": "{{ value_json.temperature}}",
            "unique_id": "rfx_{}_{}_temp".format(self.ident, self.unit),
            "device": {
                "identifiers": ["{}".format(self.ident)],
                #     "manufacturer": "ME",
                "model": "Temperature and humidity sensor",
                "name": "{} - {}".format(self.room, self.name)
                if config.MQTT_ROOM_IN_NAME
                else self.name,
            },
        }

        super(Temperature, self).mqtt_send_config_object(
            cObj, config_type="sensor/temperature"
        )

        cObj = {
            "device_class": "humidity",
            # "name": "Humidity",
            # "state_topic": "rfx2mqtt/{}".format(self.id),
            "unit_of_measurement": "%",
            "value_template": "{{ value_json.humidity}}",
            "unique_id": "rfx_{}_{}_hum".format(self.ident, self.unit),
            "device": {
                "identifiers": ["{}".format(self.ident)],
                #    "manufacturer": "ME",
                "model": "Temperature and humidity sensor",
                "name": "{} - {}".format(self.room, self.name)
                if config.MQTT_ROOM_IN_NAME
                else self.name,
            },
        }
        return super(Temperature, self).mqtt_send_config_object(
            cObj, config_type="sensor/humidity"
        )
