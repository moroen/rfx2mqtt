from typing import Any, Dict
from django import http
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django_tables2 import SingleTableView
from django.db.models.query import QuerySet
from django.views.generic import CreateView, UpdateView, TemplateView
from django.urls import reverse_lazy
from django.forms import modelform_factory

from django_collapsible_table import CollapsibleTable, CollapsibleTableView

# Create your views here.
from .models import Room
from .forms import RoomFormHelper

from gui.common import FilterBoxMixin, AddButtonMixin

from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

from devices.models import Device

from django_tables2.templatetags.django_tables2 import render_table, RenderTableNode

from logging import getLogger

# class RoomListView(FilterBoxMixin, FilterView):
#     model = Room
#     template_name = "rooms/list.html"
#     filterset_class = RoomsFilter

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         myTable = RoomListTable(data=Room.objects.all())

#         print(myTable.as_html(self.request))

#         return context

log = getLogger(__name__)

from django_filters import FilterSet, CharFilter, NumberFilter
from django.db.models import Q


class DevicesFilter(FilterSet):
    q = CharFilter(method="my_custom_filter", label="Search")
    room = NumberFilter(method="room_filter")

    class Meta:
        # model = Device
        fields = ["q", "room"]

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(room__name__icontains=value)
            | Q(ident__icontains=value)
        )

    def room_filter(self, queryset, name, value):
        return queryset.filter(room=value)


class DeviceTable(CollapsibleTable):
    table_css_class = "table table-striped w-auto small"

    fields = [
        {"name": "Id", "header_css_class": "table-primary col-1"},
        {"name": "Name", "header_css_class": "col-3"},
        {"name": "Ident", "header_css_class": "col-1"},
        {"name": "Unit", "header_css_class": "col-1"},
        {"name": "State", "header_css_class": "col-6"},
    ]

    def get_queryset(self) -> QuerySet[Any]:
        return Device.objects.all().select_subclasses()

    # def render_state(self, record):
    # a   return record.id


class RoomsTable(CollapsibleTable):
    fields = [{"name": "Id", "header_css_class": "col-1"}, "name"]
    child_table_class = DeviceTable

    table_css_class = "table table-striped"

    def get_queryset(self) -> QuerySet[Any]:
        return Room.objects.all()

    def get_child_queryset(self, record) -> QuerySet[Any]:
        qs = record.devices.all().select_subclasses()
        return qs


class RoomListView(FilterBoxMixin, CollapsibleTableView):
    template_name = "rooms/list.html"
    model = Room
    table_class = RoomsTable
    filterset_class = DevicesFilter


# class TestView(TemplateView):
#     template_name = "rooms/test.html"
#     table = None

#     def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
#         print(request.GET)
#         dev = DevicesFilter(
#             request.GET, queryset=Device.objects.all().select_subclasses()
#         )

#         self.table = DeviceTable(dev.qs)
#         return super().get(request, *args, **kwargs)

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context.update({"my_table": self.table.render()})
#         return context


# class RoomListView(FilterBoxMixin, AddButtonMixin, SingleTableMixin, FilterView):
#     table_class = RoomListTable
#     model = Room
#     template_name = "gui/list.html"
#     filterset_class = RoomsFilter

#     add_button_label = "Add"
#     add_button_target = "/rooms/add"
#     add_button_class = "btn-secondary"

#     def get_queryset(self) -> QuerySet[Any]:
#         return Room.objects.all()

#     def get(self, request, *args, **kwargs):
#         if request.htmx:
#             self.template_name = "widgets/table.html"
#         else:
#             self.template_name = "gui/list.html"

#         return super().get(request, *args, **kwargs)


class HelperMixin:
    def __init__(self, **kwargs: Any) -> None:
        self.template_name = "gui/modal_form.html"
        self.success_url = reverse_lazy("ROOMS:list")
        self.model = Room
        self.form_class = modelform_factory(self.model, fields="__all__")
        self.form = self.form_class()
        super().__init__(**kwargs)

    def insert_form_helper(self, additional=None):
        context = super().get_context_data()
        context.update({"helper": self.helper})
        if additional is not None:
            context.update(additional)
        return context


class RoomAddView(HelperMixin, CreateView):
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = self.insert_form_helper({"title": "Add room"})
        return context

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.helper = RoomFormHelper(self.form, target=reverse_lazy("ROOMS:add"))
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)


class RoomDetailView(HelperMixin, UpdateView):
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = self.insert_form_helper({"title": "Edit room"})
        return context

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object: Room = self.get_object()
        self.helper = RoomFormHelper(self.form, target=self.object.get_absolute_url())
        return super().get(request, *args, **kwargs)
