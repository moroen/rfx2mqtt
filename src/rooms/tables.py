from django_tables2 import Table, tables
from django.urls import reverse_lazy

from django_filters import FilterSet, CharFilter

from django.db.models import Q
from django.template.loader import render_to_string

from django.utils.html import format_html


class RoomsFilter(FilterSet):
    q = CharFilter(method="my_custom_filter", label="Search")

    class Meta:
        # model = Device
        fields = ["q"]

    def my_custom_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))


class RoomListTable(Table):
    id = tables.columns.TemplateColumn(
        template_code="{{record.id}}", attrs={"th": {"class": "col-1"}}
    )
    name = tables.columns.TemplateColumn(
        template_code="{{record.name}}", attrs={"th": {"class": "col-3"}}, linkify=True
    )

    detail = tables.columns.BooleanColumn(verbose_name="")

    child = tables.columns.ManyToManyColumn(transform=lambda room: r.name)

    class Meta:
        fields = ["id", "name", "child"]
        template_name = "widgets/table_bs5.html"
        attrs = {"class": "table table-striped"}

    def render_name(self, record):
        return render_to_string(
            "widgets/hx_link.html",
            context={
                "target": "#modals-here",
                "url": record.get_absolute_url(),
                "label": record.name,
            },
        )

    def render_detail(self, record):
        return record.devices.all().select_subclasses()
