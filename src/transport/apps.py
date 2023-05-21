from django.apps import AppConfig

import os

import sys


class TransportConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "transport"

    def ready(self) -> None:
        from . import start_transports

        if (
            os.environ.get("RUN_MAIN") == "true"
            or os.environ.get("RFX2MQTT_SERVER_GATEWAY_INTERFACE") == "wsgi"
        ):
            start_transports()
            pass

        elif os.environ.get("RFX2MQTT_SERVER_GATEWAY_INTERFACE") == "asgi":
            start_transports()

        return super().ready()
