from typing import Any
from rest_framework import serializers, viewsets
from rest_framework.fields import empty
from devices.models import Device, Switch


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

    def create(self, validated_data):
        print("create")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        target: Device = super().update(instance, validated_data)
        target.set_state()
        return target


class DeviceSerializer(InheritedModelSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
