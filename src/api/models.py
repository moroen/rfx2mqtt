from django.db import models

# import transport.mqtt as mqtt

import django_mqtt as mqtt
import django_rfx as rfx

from polymorphic.models import PolymorphicModel
from django.core.serializers.json import DjangoJSONEncoder

from json import dumps
from constance import config

import decimal

import logging

from django_rfx.models import PacketType, Protocol


# Json-classes
class json_Device:
    command_topic: str
    device: dict
    payload_off: str
    payload_on: str
    state_topic: str
    name: str
    unique_id: str
    valuetemplate: str


log = logging.getLogger("api")


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


# class DeviceType(models.Model):
#    description = models.CharField(max_length=50)
#
#    def __str__(self) -> str:
#        return self.description


class Device(PolymorphicModel):
    mqtt_topic_type = "device"

    room = models.ForeignKey(
        Room, related_name="devices", on_delete=models.CASCADE, default=1
    )
    device_protocol = models.ForeignKey(
        Protocol, on_delete=models.CASCADE, null=True, blank=True
    )
    packet_type = models.ForeignKey(
        PacketType, on_delete=models.CASCADE, default="0x03"
    )

    name = models.CharField(max_length=200, default="New device")
    ident = models.CharField(max_length=20, default="0123456")
    unit = models.CharField(max_length=10, default="1")

    created = models.DateTimeField(auto_now_add=True)
    changed = models.DateTimeField(auto_now=True)

    def get_state_topic(self) -> str:
        return "{}/{}/{}/state".format(config.MQTT_TOPIC, self.mqtt_topic_type, self.id)

    def get_command_topic(self) -> str:
        return "{}/{}/{}/set".format(config.MQTT_TOPIC, self.mqtt_topic_type, self.id)

    def __str__(self) -> str:
        return self.name

    def send_state(self, stateObj=None):
        if stateObj is not None:
            topic = self.get_state_topic()
            payload = dumps(stateObj, cls=DjangoJSONEncoder)
            mqtt.publish(topic, payload, retain=True)
        else:
            log.error("send_state stateObj empty")

    def set_state(self, state: bool):
        print(self.device_type)

        log.debug("Setting state for device {} to {}".format(self.id, state))

        if str(self.device_type).lower() == "switch":
            t = Switch.objects.get(device_id=self.id)
            t.set_state(state)
        elif str(self.device_type).lower() == "light":
            t = Light.objects.get(device_id=self.id)
            t.set_state(state)

        # rfx.switch(self.ident, self.device_protocol, state)
        # self.send_state()

    def send_config_object(self, sub_config=None, config_type=None):
        log.debug("Send config object for device {}".format(self.id))
        cObj = {
            "command_topic": self.get_command_topic(),
            "state_topic": self.get_state_topic(),
            "name": "{} - {}".format(self.room, self.name)
            if config.MQTT_ROOM_IN_NAME
            else self.name,
            "unique_id": "rfx_{}_{}".format(self.ident, self.unit),
        }

        if sub_config is not None:
            cObj.update(sub_config)

        cType = config_type.lower() if config_type is not None else "UNKNOWN"

        payload = dumps(cObj)
        topic = "{}/{}/{}/config".format(config.MQTT_TOPIC, cType, self.id)

        mqtt.publish(topic, payload, retain=True)


class StateDevice(Device):
    state = models.BooleanField(default=False)

    def set_state(self, state=None):
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

    class Meta:
        abstract = True


class Switch(StateDevice):
    mqtt_topic_type = "switch"

    def send_state(self):
        return super().send_state({"state": self.state})

    def send_config_object(self, sub_config=None, config_type=None):
        cObj = {
            "availability": [{"topic": "zigbee2mqtt/bridge/state"}],
            "json_attributes_topic": "{}/{}/set".format(config.MQTT_TOPIC, self.id),
            "payload_off": '{"state": false}',
            "payload_on": '{"state": true}',
            # "value_template": '{{ value_json.state }}'
        }

        return super().send_config_object(sub_config=cObj, config_type="Switch")


class Light(StateDevice):
    mqtt_topic_type = "light"

    brightness = models.IntegerField(default=50)

    def set_brightness(self, brightness):
        log.debug(
            "Setting brightness to {} for device {}:{} with packet_type {}".format(
                brightness, self.ident, self.unit, self.packet_type_id
            )
        )

        rfx.set_level(
            "{}:{}".format(self.ident, self.unit), self.packet_type_id, brightness
        )

    def send_state(self):
        return super().send_state({"brightness": self.brightness, "state": self.state})

    def send_config_object(self, sub_config=None, config_type=None):
        cObj = {
            "brightness": True,
            "brightness_scale": 100,
            "payload_off": False,
            "payload_on": True,
            # "value_template": '{{ value_json.state }}'
        }
        return super().send_config_object(cObj, "light")


class Sensor(Device):
    def set_state(self, state=None):
        log.debug("Sensors doesn´t do states")
        pass


class Temperature(Sensor):
    mqtt_topic_type = "sensor"

    temp = models.fields.DecimalField(
        max_digits=5, decimal_places=1, default=decimal.Decimal(20.0)
    )
    humidity = models.fields.IntegerField(null=True, blank=True)

    def send_state(self):
        stateObj = {"temperature": self.temp, "humidity": self.humidity}
        return super().send_state(stateObj)

    def send_config_object(self, sub_config=None, config_type=None):
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
                "name": "{}".format(self.name),
            },
        }

        super().send_config_object(cObj, "sensor/temperature")

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
                "name": "{}".format(self.name),
            },
        }
        return super().send_config_object(cObj, "sensor/humidity")
