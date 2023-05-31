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

from constance.signals import config_updated

# def parse_state_payload(payload) -> bool:
#     if payload.lower() == "on":
#         return True
#     if payload.lower() == "off":
#         return False


# def get_device_id(msg: MQTTMessage):
#     return msg.topic.split("/")[2]


def get_device_id(msg: MQTTMessage):
    return msg.topic.split("/")[2]


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    if old_value is None:
        return

    if key == "RFX_DEVICE":
        django_rfx.disconnect()
        sleep(2)
        django_rfx.connect(device=new_value)


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self) -> None:
        if not (
            environ.get("RUN_MAIN")
            or environ.get("RFX2MQTT_SERVER_GATEWAY_INTERFACE") == "asgi"
        ):
            return

        from constance import config

        # mqtt_connect(host=config.MQTT_HOST, port=config.MQTT_PORT)
        django_rfx.connect(device=config.RFX_DEVICE)

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
            print(ser)
            if ser.is_valid():
                ser.save()
            else:
                print("Not valid")

    send_device_configs()
