from django.apps import AppConfig
from django.dispatch import receiver

from django.core.exceptions import ObjectDoesNotExist

from django_mqtt.signals import connected
from django_mqtt import topic, MQTTClient, MQTTMessage
import django_rfx

import logging

from json import loads

log = logging.getLogger("RFXtrx")


def get_device_id(msg: MQTTMessage):
    return msg.topic.split("/")[2]


class DevicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "devices"

    def ready(self) -> None:
        super().ready()
        from constance import config
        from .models import Device, Temperature
        from .serializers import DeviceSerializer, TemperatureSerializer

        @topic(
            [
                "{}/+/+/set".format(config.MQTT_TOPIC),
            ]
        )
        def on_set_message(client: MQTTClient, userdata, msg: MQTTMessage):
            log.debug(
                "Received set on topic {} with payload {}".format(
                    msg.topic, msg.payload
                )
            )

            dev = get_device_id(msg)
            payload = loads(msg.payload)

            try:
                target = Device.objects.get_subclass(id=dev)
                ser = DeviceSerializer(target, data=payload)

                if ser.is_valid():
                    ser.save()
                else:
                    log.error("on_set_message: Unable to serialize")
            except Device.DoesNotExist:
                log.error(f"No device with id {dev}")

        @django_rfx.callback()
        def callback(event):
            if isinstance(event, django_rfx.SensorEvent):
                log.debug("Received sensor event: {}".format(event))

                packet_type = hex(event.device.packettype)
                device = event.device
                values = event.values
                ident, unit = device.id_string.split(":")

                if packet_type == "0x52":
                    data = {
                        "packet_type": packet_type,
                        "ident": ident,
                        "unit": unit,
                        "temp": values["Temperature"],
                        "humidity": values["Humidity"],
                    }

                    try:
                        target = Temperature.objects.get(ident=ident, unit=unit)
                        data.update(
                            {"devicetype": target._meta.model_name.capitalize()}
                        )
                        temp = TemperatureSerializer(target, data=data)

                        if temp.is_valid():
                            temp.save()
                        else:
                            log.error(
                                "Unable to serialize temperature device for update"
                            )
                    except Temperature.DoesNotExist:
                        temp = TemperatureSerializer(data=data)
                        if temp.is_valid():
                            temp.save()
                        else:
                            log.error(
                                "Unable to serialize temperature device for create"
                            )

            elif isinstance(event, django_rfx.ControlEvent):
                log.debug("Received control event {} - {}".format(event, event.device))
            else:
                log.debug("Received unknown event {}".format(event))


@receiver(connected)
def mqtt_on_connect(*args, **kwargs):
    from .models import Device

    aDev: Device

    for aDev in Device.objects.filter(mqtt_discover=True).select_subclasses():
        aDev.mqtt_send_config_object()
