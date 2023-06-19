from typing import Any
from django.contrib import admin
from polymorphic.admin import (
    PolymorphicParentModelAdmin,
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
)

# Register your models here.

from .models import Room, Device, Switch, Light, Sensor, Temperature


class DeviceChildAdmin(PolymorphicChildModelAdmin):
    base_model = Device

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        retVal = super().save_model(request, obj, form, change)
        if hasattr(obj, "set_state"):
            obj.set_state()

        if hasattr(obj, "set_brightness"):
            obj.set_brightness()
        return retVal


@admin.register(Switch)
class SwitchAdmin(DeviceChildAdmin):
    base_model = Switch
    list_display = ["name", "room", "ident", "unit", "state"]


@admin.register(Light)
class LightAdmin(DeviceChildAdmin):
    base_model = Light
    list_display = ["name", "room", "ident", "unit"]


@admin.register(Temperature)
class TemperatureAdmin(DeviceChildAdmin):
    base_model = Temperature
    list_display = ["name", "room", "ident", "unit", "temp", "humidity"]


@admin.register(Device)
class DeviceAdmin(PolymorphicParentModelAdmin):
    base_model = Device
    child_models = (Switch, Light, Temperature)
    list_display = ["name", "room", "ident", "unit"]
    list_filter = ["room"]


@admin.register(Sensor)
class SensorAdmin(DeviceChildAdmin):
    base_model = Sensor
    list_display = ["name", "room", "ident", "unit"]


admin.site.register(Room)
# admin.site.register(DeviceType)
# admin.site.register(Device)
# admin.site.register(Light)
# admin.site.register(Switch)
