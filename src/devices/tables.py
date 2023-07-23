from django_tables2 import Table, tables
from devices.models import Device, Light, Switch, Temperature
from django.template.loader import render_to_string
from django.utils.html import format_html

from django.urls import reverse_lazy


class DeviceListTable(Table):
    id = tables.columns.TemplateColumn(template_code="{{record.id}}")
    name = tables.columns.TemplateColumn(template_code="{{record.name}}", linkify=True)
    room = tables.columns.TemplateColumn(template_code="{{record.room}}")

    state = tables.columns.BooleanColumn()

    class Meta:
        fields = ["id", "name", "room", "state"]
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-striped"}

    def render_state(self, record):
        if isinstance(record, Switch):
            return render_to_string(
                "widgets/hx_switch.html",
                context={
                    "id": record.id,
                    "state": record.state,
                    "target": reverse_lazy(
                        "API:Device-detail", kwargs={"pk": record.id}
                    ),
                },
            )
        elif isinstance(record, Temperature):
            return format_html(f"{record.temp}&deg / {record.humidity}%")
        else:
            return ""
