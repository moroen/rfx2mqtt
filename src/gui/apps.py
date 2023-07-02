from django.apps import AppConfig
import logging

log = logging.getLogger("gui")


class GuiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "gui"

    def ready(self) -> None:
        log.debug("Starting GUI")
        return super().ready()
