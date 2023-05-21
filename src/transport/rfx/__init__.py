import RFXtrx
from constance import config
import time
from rfx2mqtt.log import get_log
from socket import error as socket_error
from os.path import exists


log = get_log("RFXtrx")

core = None
modes_list = ["ac", "fineoffset"]
rfxcom_device = None


def set_state(id: str, packet_type: str, state: bool) -> bool:
    global core

    log.debug(
        "Set State - ID: {} PacketType: {} State: {}".format(id, packet_type, state)
    )

    if core is None:
        log.error("Unable to set state, not connected")
        return False

    pkt = RFXtrx.lowlevel.PACKET_TYPES[int(packet_type, 0)]()
    pkt.parse_id(0x00, id.lower())
    dev = RFXtrx.LightingDevice(pkt)
    try:
        if state:
            dev.send_on(core.transport)
        else:
            dev.send_off(core.transport)

        return True
    except BrokenPipeError:
        reconnec()
        set_state(id, packet_type, state)


def set_level(id: str, packet_type: str, level: int) -> bool:
    global core

    log.debug(
        "Set Level - ID: {} PacketType: {} Level: {}".format(id, packet_type, level)
    )

    if core is None:
        log.error("Unable to set brightness, not connected")
        return False

    pkt = RFXtrx.lowlevel.PACKET_TYPES[int(packet_type, 0)]()
    pkt.parse_id(0x00, id.lower())
    dev = RFXtrx.LightingDevice(pkt)
    try:
        dev.send_dim(core.transport, level)
    except BrokenPipeError:
        reconnec()
        set_level(id, packet_type, level)


def connect():
    if not config.RFX_ENABLE:
        log.debug("Not enabled")
        return

    from .handlers import rfx_callback

    global rfxcom_device, core

    d = config.RFX_DEVICE.split(":")
    if len(d) == 2:
        rfxcom_device = (d[0], int(d[1]))
    else:
        rfxcom_device = d[0]

    if isinstance(rfxcom_device, tuple):
        proto = RFXtrx.PyNetworkTransport
    else:
        if not exists(rfxcom_device):
            log.error("Serial device {} not found".format(rfxcom_device))
            return
        else:
            proto = RFXtrx.PySerialTransport

    log.debug("Opening rfxcom on {} with protocol {}".format(rfxcom_device, proto))

    try:
        core = RFXtrx.Core(
            rfxcom_device,
            rfx_callback,
            modes=modes_list,
            transport_protocol=proto,
        )
        log.info("RFX connected")
    except AttributeError:
        time.sleep(1)
        connect()
    except socket_error:
        print("Shite")
    # except Exception as e:
    #    print(type(e).__name__)


def reconnec():
    global core
    if core is None:
        log.debug("Reconnect - Not connected")
    else:
        log.debug("Closing connection")
        core.close_connection()
    log.debug("Reconnecting")
    connect()
