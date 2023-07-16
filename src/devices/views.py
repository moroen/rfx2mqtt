from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy

from django.forms import modelform_factory
from django.apps import apps

# Create your views here.

from django.views.generic import TemplateView, UpdateView
from django_tables2 import SingleTableView
from .tables import DeviceListTable
from .forms import DefaultFormHelper

from devices.models import Device


class DeviceList(SingleTableView):
    model = Device
    template_name = "devices/list.html"
    table_class = DeviceListTable

    def get_queryset(self) -> QuerySet[Any]:
        return Device.objects.all().select_subclasses()


class DetailView(UpdateView):
    model = Device
    # fields = "__all__"
    template_name = "devices/detail.html"
    success_url = reverse_lazy("device-list")

    def set_model(self):
        self.object: Device = self.get_object()
        self.model = apps.get_model("devices", self.object.__class__.__name__)
        self.form_class = modelform_factory(self.model, fields="__all__")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().select_subclasses()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"helper": self.helper})
        return context

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.set_model()
        self.form = self.form_class()
        self.helper = DefaultFormHelper(form=self.form, form_mode="update")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.set_model()
        self.form_class = modelform_factory(self.model, fields="__all__")

        retVal = super().post(request, *args, **kwargs)

        self.form = self.form_class(request.POST)
        if self.form.is_valid():
            if "state" in self.form.cleaned_data:
                self.object.set_state(self.form.cleaned_data["state"])

        return retVal
