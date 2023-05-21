"""
ASGI config for rfx2mqtt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rfx2mqtt.settings")
os.environ.setdefault("RFX2MQTT_SERVER_GATEWAY_INTERFACE", "asgi")


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        # Just HTTP for now. (We can add other protocols later.)
    }
)
