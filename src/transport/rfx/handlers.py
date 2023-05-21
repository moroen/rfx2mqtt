from rfx2mqtt.log import get_log
import RFXtrx

from django.apps import apps

from api.serializers import DeviceSerializer, TemperatureSerializer
from api.models import Device, Temperature

from constance import config

log = get_log("RFXtrx.handlers")


def int_to_hex(value) -> str:
    return "0x{:02x}".format(value)


def create_or_update(packet_type, event):
    id = event.device.id_string.split(":")
    ident = id[0]
    unit = id[1]

    if packet_type == 0x52:  # TempHum
        if "Temperature" in event.values:
            temp = event.values["Temperature"]

        if "Humidity" in event.values:
            humidity = event.values["Humidity"]

        try:
            t = Temperature.objects.get(ident=ident, unit=unit)
            # Exists
            ser = TemperatureSerializer(t, data={"temp": temp, "humidity": humidity})
            if ser.is_valid():
                tempDevice = ser.save()
            else:
                log.error("Non-valid temperature+humididy serializer")

        except Device.DoesNotExist:
            if not config.RFX_ADD_UNKNOWN:
                log.debug("Unknown sensor received, add unknown disabled")
                return

            log.debug(
                "Creating new device width packet_type {}".format(
                    int_to_hex(packet_type)
                )
            )
            ser = TemperatureSerializer(
                data={
                    "name": "New sensor device",
                    "ident": ident,
                    "unit": unit,
                    "packet_type": int_to_hex(packet_type),
                    "temp": temp,
                    "humidity": humidity,
                }
            )

            ser.is_valid()
            tempDevice = ser.save()
            # tempDevice.send_config_object()
            # tempDevice.send_state()

    else:
        log.error("Unknown packet_type")


def rfx_callback(event):
    if isinstance(event, RFXtrx.SensorEvent):
        log.debug("Received sensor event: {}".format(event))
        packet_type = event.device.packettype
        create_or_update(packet_type, event)
    elif isinstance(event, RFXtrx.ControlEvent):
        log.debug("Received control event {} - {}".format(event, event.device))
    else:
        log.debug("Received unknown event {}".format(event))
