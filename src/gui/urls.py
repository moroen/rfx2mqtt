from django.urls import path
from django.views.generic import TemplateView

from .views import Main, SettingsView

urlpatterns = [
    path("settings/", SettingsView.as_view(), name="settings-view"),
]
