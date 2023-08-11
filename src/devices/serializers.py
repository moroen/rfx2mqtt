from rest_framework import serializers

from django.apps import apps

from .models import Temperature, Device, Switch


def modelserializer_factory(
    model, class_name="ModelFactorySerializer", meta_cls=None, **kwargs
):
    """Generate a ModelSerializer based on Model"""

    if meta_cls is None:
        # Create a Meta class with the model passed
        meta_cls = type("Meta", (object,), dict(model=model))
    elif not hasattr(meta_cls, "model"):
        # If a meta_cls is provided but did not include a model,
        # set it to the model passed into this function
        meta_cls.model = model

    # Create the ModelSerializer class with the Meta subclass
    # we created above; also pass in any additional keyword
    # arguments via kwargs
    ModelFactorySerializer = type(
        class_name, (serializers.ModelSerializer,), dict(Meta=meta_cls, **kwargs)
    )
    ModelFactorySerializer.__class__.__name__ = class_name
    return ModelFactorySerializer


class InheritedModelSerializerMixin:
    def to_representation(self, instance):
        model = instance._meta.model
        self.Meta.model = model

        serializer = modelserializer_factory(
            model, self.__class__.__name__, meta_cls=self.Meta
        )

        return serializer(instance=instance).data

    def to_internal_value(self, data):
        if self.instance is not None:
            self.Meta.model = apps.get_model(
                "devices", self.instance.__class__.__name__
            )
        return super().to_internal_value(data)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        target: Device = super().update(instance, validated_data)
        target.set_state()
        target.mqtt_send_state()
        return target


class TemperatureSerializer(InheritedModelSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"


class DeviceSerializer(InheritedModelSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"

    def to_internal_value(self, data):
        print(self.instance)
        return super().to_internal_value(data)
