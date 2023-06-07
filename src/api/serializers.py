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
    def create(self, validated_data):
        temp = super().create(validated_data)
        return temp

    class Meta:
        model = Temperature
        fields = "__all__"


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

        print(instance.polymorphic_ctype)
        # print(validated_data["devicetype"])

        cType = instance.polymorphic_ctype

        obj = cType.get_object_for_this_type(device_ptr_id=instance.id)

        print(obj)

        target_ctype = ContentType.objects.get(
            app_label="api", model=validated_data["devicetype"].lower()
        )

        if instance.polymorphic_ctype != target_ctype:
            log.debug("Devicetype Changed")

            Light.objects.create(device_ptr_id=instance.id)

            obj = cType.get_object_for_this_type(device_ptr_id=instance.id)

            print(obj.polymorphic_ctype)

            obj.delete(parent=False)

            # Light(id=1).create()
            # obj = Switch.objects.get(device_ptr_id=1)
            # obj.delete()

            # obj.delete()

        return super().update(instance, validated_data)


# class LightSerializer(serializers.ModelSerializer):
#     # device = serializers.SlugRelatedField(slug_field="name", read_only=True)
#     def update(self, instance, validated_data):
#         log.debug("LightSerializer - update with {}".format(validated_data))
#         if "state" in validated_data:
#             self.instance.set_state(validated_data["state"])

#         if "level" in validated_data and not validated_data["state"]:
#             # self.instance.set_level(validated_data["level"])
#             pass

#         return super().update(instance, validated_data)


#     class Meta:
#         model = Light
#         fields = ["device", "level", "state"]


# class SwitchSerializer(serializers.ModelSerializer):

#     device = serializers.SlugRelatedField(slug_field="name", read_only=True)

#     def update(self, instance, validated_data):
#        if "state" in validated_data:
#            self.instance.set_state(validated_data["state"])
#        return super().update(instance, validated_data)

#     class Meta:
#         model = Switch
#         fields = ["device", "state"]


# class DeviceSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(required=False)

#     def is_valid(self, *, raise_exception=False):
#         return super().is_valid(raise_exception=raise_exception)

#     def create_sub_device(self, instance):
#         if str(instance.device_type).lower() == "switch":
#             log.debug("Serializing new switch")
#             ser = SwitchSerializer(data={"device": instance.id})
#             if ser.is_valid():
#                 ser.save()
#             else:
#                 log.error("Unable to seralize switch")
#         elif str(instance.device_type).lower() == "light":
#             log.debug("Serializing new light")

#             print(instance.id)

#             ser = LightSerializer(data={"device": instance.id})
#             if ser.is_valid():
#                 ser.save()
#             else:
#                 log.error("Unable to seralize light")


#     def create(self, validated_data):
#         log.debug("Creating new device with data: {}".format(validated_data))

#         if not "ident" in validated_data:
#             validated_data["ident"] = token_hex(3)

#         newDevice = super().create(validated_data)
#         self.create_sub_device(newDevice)

#         return newDevice

#     def update(self, instance, validated_data):
#         print("called", validated_data)

#         if validated_data["device_type"] != instance.device_type:
#             log.debug("DeviceType changed")


#             try:
#                 if str(instance.device_type).lower()=="switch":
#                     oldDev = Switch.objects.get(device_id=instance.id)
#                 elif str(instance.device_type).lower() == "light":
#                     oldDev = Light.objects.get(device_id=instance.id)
#                 oldDev.delete(keep_parents=True)
#             except ObjectDoesNotExist:
#                 log.error("Unable to remove old SubDevice")

#             updatedDevice = super().update(instance, validated_data)
#             self.create_sub_device(updatedDevice)
#             return updatedDevice

#         return super().update(instance, validated_data)

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         try:
#             if str(instance.device_type).lower() == "switch":
#                 t = Switch.objects.get(device_id=instance.id)
#                 representation["status"] = {"state": t.state}
#             elif str(instance.device_type).lower() == "light":
#                 t = Light.objects.get(device_id=instance.id)
#                 representation["status"] = {"state": t.state, "level": t.level}
#         except ObjectDoesNotExist:
#             log.error("No match for device id {}".format(instance.id))
#             representation["status"] = None

#         return representation

#     def to_internal_value(self, data):
#         log.debug("to_internal_value with data: {}".format(data))

#         if "status" in data:
#             if "state" in data["status"]:
#                 self.instance.set_state(data["status"]["state"])

#         return super().to_internal_value(data)

#     class Meta:
#         model = Device
#         fields = [
#             "id",
#             "name",
#             "room",
#             "device_type",
#             "device_sub_type",
#             "packet_type",
#             "ident",
#             "unit",
#         ]


# class RoomDetailSerializer(serializers.ModelSerializer):
#     devices = serializers.SlugRelatedField(slug_field="name", many=True, read_only=True)

#     # devices = DeviceSerializer(many=True, read_only=True)

#     class Meta:
#         model = Room
#         fields = ["id", "name", "devices"]


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
    

