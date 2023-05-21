"""
WSGI config for rfx2mqtt project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rfx2mqtt.settings")
os.environ.setdefault("RFX2MQTT_SERVER_GATEWAY_INTERFACE", "wsgi")

application = get_wsgi_application()
