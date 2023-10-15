# Create your views here.

from typing import Any, Dict
from django.http import HttpRequest, HttpResponse, QueryDict
from django.views.generic import TemplateView, FormView, UpdateView
from constance.admin import ConstanceForm

from django.urls import reverse_lazy

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from constance import config
from django.conf import settings


from operator import itemgetter

from django.utils.formats import localize
from django.views.generic.edit import FormView

# from django.utils.translation import ugettext_lazy as _


from constance import settings, LazyConfig
from constance.admin import ConstanceForm

from .forms import SettingsForm

from django_collapsible_table import hx_table_view, CollapsibleTable


from devices.tables import DevicesTable


def TestTable(CollapsibleTable):
    pass


# class hx_table(hx_table_view):
#    tables = {
#        "Devices": DevicesTable,
#    }


class Main(TemplateView):
    template_name = "index.html"


class SettingsFormHelper(FormHelper):
    def __init__(self, form=None):
        super().__init__(form)
        self.form_method = "post"

        self.form_class = "form-horizontal ms-3 mt-3"
        self.label_class = "col-lg-2"
        self.field_class = "col-lg-4"

        self.add_input(Submit("submit", "Save", css_class="btn-primary"))


config = LazyConfig()


class TestView(TemplateView):
    template_name = "test.html"


class SettingsView(FormView):
    form_class = SettingsForm
    template_name = "gui/settings.html"
    success_url = reverse_lazy("DEVICES:list")

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

    def form_valid(self, form: Any) -> HttpResponse:
        form.save()
        return super().form_valid(form)


# class ConstanceConfigView(FormView):
#     form_class = ConstanceForm
#     template_name = "gui/settings.html"
#     success_url = reverse_lazy("device-list")

#     def __init__(self, *args, **kwargs):
#         if "fields" in kwargs:
#             self.fields = kwargs.pop("fields")
#         else:
#             self.fields = settings.CONFIG.keys()
#         super(ConstanceConfigView, self).__init__(*args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super(ConstanceConfigView, self).get_context_data(**kwargs)
#         context["helper"] = SettingsFormHelper()
#         context["config"] = []
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         initial = self.get_initial()
#         for name, (default, help_text) in settings.CONFIG.items():
#             value = initial.get(name)
#             if value is None:
#                 value = getattr(config, name)
#             context["config"].append(
#                 {
#                     "name": name,
#                     "default": localize(default),
#                     "help_text": localize(help_text),
#                     "value": localize(value),
#                     "modified": value != default,
#                     "form_field": form[name],
#                     "is_checkbox": isinstance(value, bool),
#                 }
#             )
#         context["config"].sort(key=itemgetter("name"))
#         return context

#     def get_initial(self):
#         data = super(ConstanceConfigView, self).get_initial()
#         default_initial = (
#             (name, default)
#             for name, (default, help_text) in settings.CONFIG.items()
#             if name in self.fields
#         )
#         initial = dict(
#             default_initial,
#             **dict(
#                 config._backend.mget(
#                     [k for k in settings.CONFIG.keys() if k in self.fields]
#                 )
#             )
#         )
#         data.update(initial)
#         return data

#     def form_valid(self, form):
#         print(form)
#         form.save()
#         return super(ConstanceConfigView, self).form_valid(form)


def get_setting(request):
    return HttpResponse("Test")


# class SettingsView(FormView):
#     form_class = ConstanceForm
#     template_name = "gui/settings.html"
#     success_url = reverse_lazy("device-list")

#     def __init__(self, **kwargs: Any) -> None:
#         self.fields = getattr(settings, "CONSTANCE_CONFIG", {})
#         self.helper = SettingsFormHelper()
#         super().__init__(**kwargs)

#     def get_initial(self) -> Dict[str, Any]:
#         init = super().get_initial()

#         for field in self.fields:
#             init.update({field: getattr(config, field)})

#         return init

#     def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context.update({"helper": self.helper})
#         return context

#     def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
#         # form = self.get_form(self.form_class)

#         return super().get(request, *args, **kwargs)
#         # self.helper = FormHelper(self)

#     def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
#         data = ConstanceForm(request.POST.copy()).cleaned_data

#         form = ConstanceForm(request.POST.copy())

#         print(form.cleaned_data)

#         # for field in validForm.fields:
#         #     currentValue = getattr(config, field, None)
#         #     print(field, currentValue)
#         #     if currentValue is not None:
#         #         newValue = data.get(field, None)
#         #         print(newValue)
#         #         if newValue != currentValue:
#         #             setattr(config, field, newValue)

#         return super().post(request, *args, **kwargs)
