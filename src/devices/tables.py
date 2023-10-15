from django_tables2 import Table, tables

from django_tables2.views import SingleTableMixin, SingleTableView
from django_filters import FilterSet, CharFilter, NumberFilter
from django_filters.views import FilterView

from devices.models import Device, Light, Switch, Temperature
from django.template.loader import render_to_string
from django.utils.html import format_html

from django.urls import reverse_lazy

from django.db.models import Q

from django_collapsible_table import CollapsibleTable, hx_table

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


@hx_table
class DevicesTable(CollapsibleTable):
    table_css_class = "table  w-auto small"
    filterset_class = DevicesFilter
    template_name = "rooms/list.html"

    fields = [
        {"name": "Id", "width": 1},
        {"name": "Name", "width": 2},
        {"name": "Ident", "width": 1},
        {"name": "Unit", "width": 1},
        {"name": "Room", "width": 1},
        {"name": "State", "width": 2, "sortable": False},
    ]

    key = "id"
    foreign_key = "room"

    def get_queryset(self) -> QuerySet[Any]:
        return Device.objects.all().select_subclasses()

    def sort_room(self, queryset: QuerySet, order=None):
        if order == "desc":
            return queryset.order_by("room__name").reverse()
        else:
            return queryset.order_by("room__name")
