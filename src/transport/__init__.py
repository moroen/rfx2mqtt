import sys

sys.path.append("../")

from rfx2mqtt.log import get_log
import transport.mqtt as mqtt
import transport.rfx as rfx

from django.dispatch import receiver
from constance.signals import config_updated
from constance import config

log = get_log("Transport")


@receiver(config_updated)
def constance_updated(sender, key, old_value, new_value, **kwargs):
    # print(sender, key, old_value, new_value)

    if "MQTT" in key:
        if old_value is not None:
            log.debug("MQTT-config changed")
            mqtt.restart()

    if "RFX" in key:
        if old_value is not None:
            log.debug("RFX-config changed")
            rfx.reconnec()


def start_transports():
    log.debug("Starting transports")

    if config.RFX_ENABLE:
        # log.debug("Starting RFX")
        # rfx.connect()
        pass
    else:
        log.debug("RFX disabled")

    if config.MQTT_ENABLE:
        # log.debug("Staring MQTT")
        # mqtt.connect()
        pass
    else:
        log.debug("MQTT disabled")
