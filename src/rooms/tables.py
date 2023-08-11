from django_tables2 import Table, tables
from django.urls import reverse_lazy


class RoomListTable(Table):
    id = tables.columns.TemplateColumn(template_code="{{record.id}}")
    name = tables.columns.TemplateColumn(template_code="{{record.name}}", linkify=True)

    class Meta:
        fields = ["name"]
        template_name = "django_tables2/bootstrap.html"
        attrs = {"class": "table table-striped"}
