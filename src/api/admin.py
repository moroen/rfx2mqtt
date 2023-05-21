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


@admin.register(Switch)
class SwitchAdmin(DeviceChildAdmin):
    base_model = Switch


@admin.register(Light)
class LightAdmin(DeviceChildAdmin):
    base_model = Light


@admin.register(Temperature)
class TemperatureAdmin(DeviceChildAdmin):
    base_model = Temperature


@admin.register(Device)
class DeviceAdmin(PolymorphicParentModelAdmin):
    base_model = Device
    child_models = (Switch, Light, Temperature)


@admin.register(Sensor)
class SensorAdmin(DeviceChildAdmin):
    base_model = Sensor


admin.site.register(Room)
# admin.site.register(DeviceType)
# admin.site.register(Device)
# admin.site.register(Light)
# admin.site.register(Switch)
