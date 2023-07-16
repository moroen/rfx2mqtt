from django.urls import path
from django.views.generic import TemplateView

from .views import Main, ConstanceConfigView, get_setting

urlpatterns = [
    path("settings/", ConstanceConfigView.as_view(), name="settings-view"),
    path("settings/value", get_setting, name="settings-value"),
]
