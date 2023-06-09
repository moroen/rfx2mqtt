from django.apps import AppConfig
from django.dispatch import receiver
import logging

from django_mqtt import (
    connect as mqtt_connect,
    topic,
    MQTTMessage,
    MQTTClient,
    on_connect,
)
from django_mqtt.signals import connected

import django_rfx

from json import loads
from os import environ
from time import sleep


log = logging.getLogger("api")

# def parse_state_payload(payload) -> bool:
#     if payload.lower() == "on":
#         return True
#     if payload.lower() == "off":
#         return False


# def get_device_id(msg: MQTTMessage):
#     return msg.topic.split("/")[2]


def get_device_id(msg: MQTTMessage):
    return msg.topic.split("/")[2]


@django_rfx.callback()
def callback(event):
    if isinstance(event, django_rfx.SensorEvent):
        log.debug("Received sensor event: {}".format(event))
        from .serializers import TemperatureSerializer

        packet_type = hex(event.device.packettype)
        device = event.device
        values = event.values
        ident, unit = device.id_string.split(":")

        if packet_type == "0x52":
            from .models import Device
            from api.serializers import DevicePolymorphicSerializer

            data = {
                "packet_type": packet_type,
                "ident": ident,
                "unit": unit,
                "temp": values["Temperature"],
                "humidity": values["Humidity"],
            }

            try:
                target = Device.objects.get(ident=ident, unit=unit)
                data.update({"devicetype": target._meta.model_name.capitalize()})
                temp = DevicePolymorphicSerializer(target, data=data)

                if temp.is_valid():
                    temp.save()
                else:
                    log.error("Unable to serialize temperature device for update")
            except Device.DoesNotExist:
                temp = TemperatureSerializer(data=data)
                if temp.is_valid():
                    temp.save()
                else:
                    log.error("Unable to serialize temperature device for create")

    elif isinstance(event, django_rfx.ControlEvent):
        log.debug("Received control event {} - {}".format(event, event.device))
    else:
        log.debug("Received unknown event {}".format(event))


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self) -> None:
        if not (
            environ.get("RUN_MAIN")
            or environ.get("RFX2MQTT_SERVER_GATEWAY_INTERFACE") == "asgi"
        ):
            return

        return super().ready()


def send_device_configs():
    from .models import Device

    devices = Device.objects.all()
    for dev in devices:
        dev.send_config_object()
        dev.send_state()


@receiver(connected)
def on_connected(*args, **kwargs):
    from constance import config

    @topic(
        [
            "{}/+/+/set".format(config.MQTT_TOPIC),
        ]
    )
    def on_set_message(client: MQTTClient, userdata, msg: MQTTMessage):
        from api.models import Device
        from api.serializers import DevicePolymorphicSerializer
        from django.contrib.contenttypes.models import ContentType

        log.debug(
            "Received set on topic {} with payload {}".format(msg.topic, msg.payload)
        )

        dev = get_device_id(msg)

        if dev is None:
            log.error("Illegal device")
        else:
            tDevice = Device.objects.get(pk=dev)
            payload = loads(msg.payload)

            ct = tDevice._meta.model_name.capitalize()
            payload.update({"devicetype": ct})

            ser = DevicePolymorphicSerializer(
                tDevice,
                data=payload,
            )
     
            if ser.is_valid():
                ser.save()
            else:
                log.error("on_set_message: Unable to serialize")

    send_device_configs()
