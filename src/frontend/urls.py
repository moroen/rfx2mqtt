from django.urls import path
from django.views.generic import TemplateView

from .views import MainView

app_name = "frontend"

urlpatterns = [
    path("", MainView.as_view(), name="index"),
]
