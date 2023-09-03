from typing import Any, Dict
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.urls import reverse_lazy

from django.forms import modelform_factory
from django.apps import apps

# Create your views here.

from django.views.generic import TemplateView, UpdateView, DeleteView, CreateView
from django_tables2 import SingleTableView
from .forms import DeviceFormHelper

from devices.models import Device

from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

from gui.common import FilterBoxMixin, AddButtonMixin

from django_collapsible_table import CollapsibleTable, CollapsibleTableView

from .tables import DevicesFilter, DevicesTable


class DeviceListView(FilterBoxMixin, AddButtonMixin, CollapsibleTableView):
    template_name = "gui/table.html"
    table_class = DevicesTable
    filterset_class = DevicesFilter

    add_button_label = "Add"
    add_button_target = "/devices/add"
    add_button_class = "btn-secondary"

    def get_queryset(self) -> QuerySet[Any]:
        return Device.objects.all().select_subclasses()


# class DeviceListView(FilterBoxMixin, AddButtonMixin, SingleTableMixin, FilterView):
#     table_class = DeviceListTable
#     model = Device
#     template_name = "gui/list.html"
#     filterset_class = DevicesFilter

#     add_button_label = "Add"
#     add_button_target = "/devices/add"
#     add_button_class = "btn-secondary"

#     exclude = None

#     def get_table_kwargs(self):
#         return {"exclude": (self.exclude)}

#     def get_queryset(self) -> QuerySet[Any]:
#         return Device.objects.all().select_subclasses()

#     def get(self, request, *args, **kwargs):
#         if "exclude" in request.GET:
#             self.exclude = request.GET["exclude"]

#         if request.htmx:
#             self.template_name = "widgets/table.html"
#         else:
#             self.template_name = "gui/list.html"

#         return super().get(request, *args, **kwargs)


class DeviceAddView(CreateView):
    def __init__(self, **kwargs: Any) -> None:
        self.template_name = "devices/add.html"
        self.success_url = reverse_lazy("DEVICES:list")
        super().__init__(**kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"helper": self.helper, "modal_extra_css": "modal-lg"})
        return context

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        print(request.GET)

        if "devicetype" in request.GET:
            self.model = apps.get_model("devices", request.GET["devicetype"])
            self.template_name = "widgets/crispy_form.html"
        else:
            self.model = apps.get_model("devices", "Switch")
            self.template_name = "devices/add.html"

        self.form_class = modelform_factory(self.model, fields="__all__")
        self.form = self.form_class()

        self.helper = DeviceFormHelper(
            form=self.form, form_mode="add", devicetype=self.model.__name__
        )

        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        data = request.POST
        self.fields = "__all__"
        self.model = apps.get_model("devices", data["devicetype"])
        return super().post(request, *args, **kwargs)


class DeviceDeleteView(DeleteView):
    def __init__(self, **kwargs: Any) -> None:
        self.model = Device
        self.success_url = reverse_lazy("DEVICES:list")
        self.template_name = "devices/delete.html"
        super().__init__(**kwargs)


class DetailView(UpdateView):
    model = Device
    template_name = "gui/modal_form.html"
    success_url = reverse_lazy("DEVICES:list")

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
        context.update({"helper": self.helper, "title": "Details"})
        return context

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.set_model()
        self.form = self.form_class()
        self.helper = DeviceFormHelper(form=self.form, form_mode="update")
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.set_model()
        self.form_class = modelform_factory(self.model, fields="__all__")

        retVal = super().post(request, *args, **kwargs)
        self.object.set_state()
        return retVal
