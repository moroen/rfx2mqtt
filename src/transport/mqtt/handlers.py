from constance import config
import paho.mqtt.client as mqtt_lib
from json import loads


from rfx2mqtt.log import get_log


log = get_log("MQTT.handlers")


def parse_state_payload(payload) -> bool:
    if payload.lower() == "on":
        return True
    if payload.lower() == "off":
        return False


def send_device_configs():
    from api.models import Device

    devices = Device.objects.all()
    for dev in devices:
        dev.send_config_object()
        dev.send_state()


def get_device_id(msg: mqtt_lib.MQTTMessage):
    return msg.topic.split("/")[2]


def on_fail(client, userdata, flags, rc):
    log.error("Connection failed")


def on_message(client, userdata, msg: mqtt_lib.MQTTMessage):
    log.debug("Received {} on topic {}".format(msg.payload, msg.topic))


def on_set_message(client, userdata, msg: mqtt_lib.MQTTMessage):
    from api.models import Device
    from api.serializers import DevicePolymorphicSerializer
    from django.contrib.contenttypes.models import ContentType

    log.debug("Received set on topic {} with payload {}".format(msg.topic, msg.payload))

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

        # if state is not None:
        #    tDevice.set_state(state)
        # if brightness is not None:
        #    tDevice.set_level(brightness)


def on_device_message(client, userdata, msg: mqtt_lib.MQTTMessage):
    log.debug("Received device topic {} with payload {}".format(msg.topic, msg.payload))
    parts = msg.topic.split("/")

    cmd = parts[2]
    data = loads(msg.payload)
    if cmd == "new":
        log.debug("Creating new device with data {}".format(data))
        from api.serializers import DeviceSerializer

        dev = DeviceSerializer(data=data)
        dev.is_valid()
        dev.save()
    elif cmd == "delete":
        from api.models import Device

        dev = Device.objects.get(id=data["id"])
        dev.delete()
    else:
        log.error("Unknown device-command {}".format(cmd))
        pass
