from django.apps import AppConfig
from django.dispatch import receiver
import logging

from django_mqtt import topic, MQTTMessage, MQTTClient
from django_mqtt.signals import connected

from json import loads

log = logging.getLogger("api")


def parse_state_payload(payload) -> bool:
    if payload.lower() == "on":
        return True
    if payload.lower() == "off":
        return False


def get_device_id(msg: MQTTMessage):
    return msg.topic.split("/")[2]


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self) -> None:
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
                "Received set on topic {} with payload {}".format(
                    msg.topic, msg.payload
                )
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

        return super().ready()


def send_device_configs():
    from .models import Device

    devices = Device.objects.all()
    for dev in devices:
        dev.send_config_object()
        dev.send_state()


@receiver(connected)
def is_connected(**kwargs):
    from constance import config

    log.debug("Received connected signal")
    send_device_configs()
