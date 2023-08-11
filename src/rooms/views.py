from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from django_tables2 import SingleTableView
from django.db.models.query import QuerySet
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from django.forms import modelform_factory

# Create your views here.
from .models import Room
from .tables import RoomListTable
from .forms import RoomFormHelper


class RoomList(SingleTableView):
    model = Room
    template_name = "gui/list.html"
    table_class = RoomListTable

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "functionbar_right": render_to_string(
                    "widgets/hx_popup_button.html",
                    {
                        "label": "Add",
                        "target": "/rooms/add",
                        "button_class": "btn-secondary",
                    },
                ),
            }
        )
        return context

    def get_queryset(self) -> QuerySet[any]:
        return Room.objects.all()


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
