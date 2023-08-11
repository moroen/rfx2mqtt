"""
ASGI config for rfx2mqtt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rfx2mqtt.settings")
os.environ.setdefault("RUN_MAIN", "true")

application = get_asgi_application()
