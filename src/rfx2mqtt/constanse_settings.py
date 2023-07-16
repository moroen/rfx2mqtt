CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = {
    "MQTT_HOST": ("127.0.0.1", ""),
    "MQTT_PORT": (1883, ""),
    "MQTT_ENABLE": (True, ""),
    "MQTT_TOPIC": ("rfx2mqtt", ""),
    "MQTT_ROOM_IN_NAME": (False, "Include room in device discovery name"),
    "RFX_ENABLE": (True, "Enable RFX"),
    "RFX_DEVICE": ("/dev/ttyAMC0", ""),
    "RFX_DEFAULT_PACKET_TYPE": ("0x03", ""),
    "RFX_SWITCH_ON_CREATE": (True, "Send a ON-command after adding new device"),
    "RFX_ADD_UNKNOWN": (True, "Add new devices on events"),
    "RFX_SWITCH_ON_LEVEL_SET": (True, "Set state to True on level change"),
}
