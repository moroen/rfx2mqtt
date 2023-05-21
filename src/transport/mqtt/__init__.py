import paho.mqtt.client as mqtt_lib
from rfx2mqtt.log import get_log
from random import randint
from constance import config
from constance.signals import config_updated
from json import loads
from logging import Logger

from django.dispatch import receiver
from transport.mqtt.handlers import (
    on_fail,
    on_message,
    on_set_message,
    on_device_message,
)

client: mqtt_lib.Client = None
client_id = None
host: str = None
port: int = None
do_restart = False

log = get_log("MQTT-old")


def connect() -> None:
    global host, port, client, log
    log.debug("Init client")

    host = config.MQTT_HOST
    port = config.MQTT_PORT

    client = mqtt_lib.Client(f"python-mqtt-{randint(0, 1000)}")
    client.on_connect = on_connect
    client.on_connect_fail = on_fail
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.loop_start()
    client.connect(host, port)


def on_connect(client: mqtt_lib.Client, userdata, flags, rc):
    from .handlers import send_device_configs

    topics = [
        # ("{}/+/set".format(config.MQTT_TOPIC), on_set_message),
        ("{}/+/+/set".format(config.MQTT_TOPIC), on_set_message),
        ("{}/device/#".format(config.MQTT_TOPIC), on_device_message),
    ]

    log.info("Connected to {}:{}".format(host, port))

    for topic, handler in topics:
        log.debug("Subscribing to {}".format(topic))
        client.subscribe(topic, 1)
        client.message_callback_add(topic, handler)

    send_device_configs()


def on_disconnect(client: mqtt_lib.Client, userdata, rc):
    global do_restart
    log.info("Disconnected")
    if do_restart:
        do_restart = False
        connect()


def restart() -> None:
    global do_restart

    if client is not None:
        if client.is_connected() and config.MQTT_ENABLE:
            do_restart = True
            client.disconnect()
        elif not client.is_connected() and config.MQTT_ENABLE:
            client.connect()
    else:
        if config.MQTT_ENABLE:
            connect()


def send(topic: str, payload: str, retain=False, qos=0) -> bool:
    global log

    print("Transport MQTT removed")

    log.debug("Sending {} on topic {} with retain: {}".format(payload, topic, retain))

    if client is None:
        log.error("Unable to publish, not connected")
        return False

    client.publish(topic, payload, retain=retain, qos=qos)
    return True
