from django.urls import path
from django.views.generic import TemplateView

from .views import Main, SettingsView, TestView

from django_collapsible_table import hx_table_view

urlpatterns = [
    path("test/", TestView.as_view(), name="testing-view"),
    path("settings/", SettingsView.as_view(), name="settings-view"),
    path("tables/<tablename>", hx_table_view.as_view(), name="table-view"),
]
