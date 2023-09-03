from django_tables2 import Table, tables

from django_tables2.views import SingleTableMixin, SingleTableView
from django_filters import FilterSet, CharFilter, NumberFilter
from django_filters.views import FilterView

from devices.models import Device, Light, Switch, Temperature
from django.template.loader import render_to_string
from django.utils.html import format_html

from django.urls import reverse_lazy

from django.db.models import Q

from django_collapsible_table import CollapsibleTable

from typing import Any, Dict

from django.db.models.query import QuerySet


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


class DevicesTable(CollapsibleTable):
    table_css_class = "table table-striped w-auto small"

    fields = [
        {"name": "Id", "header_css_class": "col-1"},
        {"name": "Name", "header_css_class": "col-3"},
        {"name": "Ident", "header_css_class": "col-1"},
        {"name": "Unit", "header_css_class": "col-1"},
        {"name": "Room", "header_css_class": "col-2"},
        {"name": "State", "header_css_class": "col-4"},
    ]

    def get_queryset(self) -> QuerySet[Any]:
        return Device.objects.all().select_subclasses()


# class DeviceListTable(Table):
#     id = tables.columns.TemplateColumn(
#         template_code="{{record.id}}", attrs={"th": {"class": "col-1"}}
#     )
#     name = tables.columns.TemplateColumn(
#         template_code="{{record.name}}", attrs={"th": {"class": "col-3"}}
#     )
#     ident = tables.columns.TemplateColumn(
#         template_code="{{record.ident}}", attrs={"th": {"class": "col-1"}}
#     )

#     unit = tables.columns.TemplateColumn(
#         template_code="{{record.unit}}", attrs={"th": {"class": "col-1"}}
#     )
#     room = tables.columns.TemplateColumn(
#         template_code="{{record.room}}", attrs={"th": {"class": "col-2"}}
#     )

#     state = tables.columns.BooleanColumn()

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     class Meta:
#         fields = ["id", "name", "ident", "unit", "room", "state"]
#         template_name = "django_tables2/bootstrap5.html"
#         attrs = {"class": "table table-striped"}

#     def render_state(self, record):
#         return record.render_widget()

#     def render_name(self, record):
#         return render_to_string(
#             "widgets/hx_link.html",
#             context={
#                 "target": "#modals-here",
#                 "url": record.get_absolute_url(),
#                 "label": record.name,
#             },
#         )
