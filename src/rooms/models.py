from django.db import models
from django.urls import reverse
from django.utils.html import format_html

# Create your models here.

""


class CollapsibleTableModelMixin:
    def render_row(self):
        return "row"

    def render_header(self):
        return format_html("<th>Test</th>")


class Room(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("ROOMS:detail", kwargs={"pk": self.id})
