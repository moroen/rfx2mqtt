from .models import Room
from django_collapsible_table import hx_table, CollapsibleTable
from django_filters import FilterSet, CharFilter
from django_tables2 import Table, tables
from django.db.models import Q
from django.db.models.query import QuerySet
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import format_html
from typing import Any, Dict

from devices.tables import DevicesTable


class RoomsFilter(FilterSet):
    q = CharFilter(method="my_custom_filter", label="Search")

    class Meta:
        # model = Device
        fields = ["q"]

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))


@hx_table
class DevicesByRoomTable(DevicesTable):
    foreign_key = "room"
    pass


@hx_table
class RoomsTable(CollapsibleTable):
    fields = [{"name": "Id", "width": 1}, "name"]

    child_table_class = DevicesByRoomTable
    filtersset_class = RoomsFilter
    template_name = "rooms/list.html"

    key = "id"

    def get_queryset(self) -> QuerySet[Any]:
        return Room.objects.all()

    def get_child_queryset(self, record) -> QuerySet[Any]:
        return record.devices.all().select_subclasses()
