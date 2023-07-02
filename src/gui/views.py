from typing import Any, Dict
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View, FormView
import django_tables2 as tables
from django.template.loader import render_to_string
from django.http import HttpRequest, HttpResponse, QueryDict
from django.apps import apps
from django.urls import reverse

from django.utils.html import format_html

from django.views.generic.edit import CreateView, DeleteView, UpdateView

import logging

from django.forms import formset_factory


log = logging.getLogger("gui")

# Create your views here.

from api.models import Device, Switch, Sensor, Light, StateDevice, Temperature
from .forms import DeviceForm, DefaultFormHelper


class TestView(ListView):
    model = Device
    template_name = "testing.html"


class DeviceTable(tables.Table):
    class Meta:
        model = Device
        template_name = "django_tables2/bootstrap.html"
        fields = ("id", "name", "room", "state")
        attrs = {"class": "table table-striped"}

    # custom = tables.Column(empty_values=())

    name = tables.Column(linkify=True)

    def render_state(self, record):
        if hasattr(record, "state"):
            return render_to_string(
                "device/switch.html", context={"id": record.id, "state": record.state}
            )
        else:
            return ""


class DeviceView(tables.SingleTableView):
    model = Device
    table_class = DeviceTable
    template_name = "device/list.html"


class TestView(CreateView):
    form = formset_factory(Switch)
    template_name = "device/detail.html"
    model = Switch
    fields = "__all__"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)


class ViewHelper:
    def set_model_properties(self, request) -> str:
        data = request.GET
        if len(data) == 0:
            self.template_name = "device/add.html"
            self.model = Switch
        else:
            if request.htmx:
                self.template_name = "device/crispy_form.htmx"
            else:
                self.template_name = "device/crispy_form.html"

            model = apps.get_model("api", data["devicetype"])
            self.model = model

        return data["devicetype"] if len(data) > 0 else "device"


class EditView(UpdateView, ViewHelper):
    pass


class AddView(CreateView, ViewHelper):
    template_name = "device/add.html"
    fields = "__all__"

    def __init__(self, **kwargs: Any) -> None:
        self.helper = DefaultFormHelper()
        self.success_url = reverse("devices-view")
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"helper": self.helper})
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        devType = self.set_model_properties(request)
        self.helper.form_action = f"{reverse('device-add-view')}?devicetype={devType}"

        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        devType = self.set_model_properties(request)
        return super().post(request, *args, **kwargs)


# class AddView(CreateView):
#     form_class = DeviceForm
#     template_name = "add.html"

#     # http_method_names = ["get", "post"]
#     # form_class = AddNewDeviceForm
#     success_url = "/gui/devices"

#     # def form_valid(self, form: Any) -> HttpResponse:
#     #     log.debug(f"AddForm valid with: {form}")
#     #     return super().form_valid(form)

#     def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
#         if request.htmx:
#             log.debug("Using htmx")
#         else:
#             log.debug("Not using htmx")
#         return super().get(request, *args, **kwargs)
