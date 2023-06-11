from rest_framework import serializers
from rest_framework.fields import empty

from django.contrib.contenttypes.models import ContentType

from rest_polymorphic.serializers import PolymorphicSerializer


from .models import Device, Room, Switch, Light, PacketType, Temperature
from constance.backends.database.models import Constance
from constance import config
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rfx2mqtt.log import get_log

from json import loads
from secrets import token_hex

log = get_log("api.serializers")


class CustomSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        log.debug("CustomSerializer_create with data: {}".format(validated_data))
        if not "ident" in validated_data:
            validated_data["ident"] = token_hex(3)

        if not "packet_type" in validated_data:
            log.debug(
                "CustomSerializer_create: Using default packet_type ({})".format(
                    config.RFX_DEFAULT_PACKET_TYPE
                )
            )
            validated_data["packet_type_id"] = config.RFX_DEFAULT_PACKET_TYPE

        newDevice = super().create(validated_data)
        newDevice.send_config_object()
        return newDevice

    def update(self, instance, validated_data):
        log.debug("CustomSerializer_update with data {}".format(validated_data))
        targetDevice = super().update(instance, validated_data)
        targetDevice.send_state()
        targetDevice.set_state()
        return targetDevice

    def is_valid(self, *args, raise_exception=False):
        return super().is_valid(raise_exception=True)


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "name"]


class DeviceSerializer(CustomSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class SwitchSerializer(CustomSerializer):
    def update(self, instance, validated_data):
        log.debug("SwitchSerializer-update")
        if "state" in validated_data:
            state = validated_data["state"]
            # instance.set_state(state)

        return super().update(instance, validated_data)

    class Meta:
        model = Switch
        fields = "__all__"


class LightSerializer(CustomSerializer):
    def update(self, instance, validated_data):
        log.debug("LightSerializer_update with data: {}".format(validated_data))

        if "brightness" in validated_data:
            instance.set_brightness(validated_data["brightness"])
            if config.RFX_SWITCH_ON_LEVEL_SET and "state" not in validated_data:
                validated_data["state"] = True
                # instance.set_state(True)

        if "state" in validated_data:
            state = validated_data["state"]
            instance.set_state(state)

        return super().update(instance, validated_data)

    class Meta:
        model = Light
        fields = "__all__"


class TemperatureSerializer(CustomSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"

    def is_valid(self, *args, raise_exception=False):
        return super().is_valid(*args, raise_exception=raise_exception)


class SensorPolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = "devicetype"
    model_serializer_mapping = {Temperature: TemperatureSerializer}


class DevicePolymorphicSerializer(PolymorphicSerializer):
    resource_type_field_name = "devicetype"
    model_serializer_mapping = {
        Device: DeviceSerializer,
        Switch: SwitchSerializer,
        Light: LightSerializer,
        Temperature: TemperatureSerializer,
    }

    class Meta:
        extra_kwargs = {
            "resourcetype": {
                "read_only": True
            }  # define the 'user' field as 'read-only'
        }

    def is_valid(self, *args, **kwargs):
        return super().is_valid(*args, raise_exception=True)

    def update(self, instance, validated_data):
        cType = instance.polymorphic_ctype
        target_ctype = ContentType.objects.get(
            app_label="api", model=validated_data["devicetype"].lower()
        )

        if instance.polymorphic_ctype != target_ctype:
            log.debug("Devicetype Changed")

            targetClass = target_ctype.model_class()

            newDev = targetClass(
                id=instance.id,
                room=instance.room,
                device_protocol=instance.device_protocol,
                packet_type=instance.packet_type,
                name=instance.name,
                ident=instance.ident,
                unit=instance.unit,
            )
            instance.delete()

            newDev.save()

            return newDev
        else:
            return super().update(instance, validated_data)

class ConfigSerializer(serializers.HyperlinkedModelSerializer):
    default = serializers.SerializerMethodField()
    # help_text = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    id = serializers.SerializerMethodField()

    class Meta:
        model = Constance
        fields = ("id", "key", "default", "value")

    def get_id(self, obj):
        return obj.key

    def get_default(self, obj):
        default, _ = settings.CONSTANCE_CONFIG.get(obj.key)
        return default

    def get_help_text(self, obj):
        _, help_text = settings.CONSTANCE_CONFIG.get(obj.key)
        return help_text

    def get_value(self, obj):
        return getattr(config, obj.key, None)
