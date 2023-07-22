from typing import Any, Optional, Sequence, Type, Union
from django import forms, conf

from constance import settings, LazyConfig
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList

from hashlib import sha256
from decimal import Decimal
from datetime import datetime, date, time, timedelta
from django.forms.widgets import Widget

from django.utils.text import normalize_newlines

from django.utils.safestring import SafeText
from django.utils import timezone

from django.template.loader import render_to_string

config = LazyConfig()


class SettingsHelper:
    def set_params(self, **kwargs):
        self.name = kwargs.pop("name")
        self.default = kwargs.pop("default")
        self.help_text = kwargs.pop("help_text")
        return kwargs

    def get_extra_context(self, **kwargs):
        context = {
            "name": self.name,
            "default": self.default,
            "help_text": self.help_text,
            "id": f"id_{self.name}",
        }
        context.update(kwargs)
        return context


class SettingsCharWidget(forms.TextInput, SettingsHelper):
    def __init__(self, **kwargs) -> None:
        super().__init__(self.set_params(**kwargs))

    def render(self, **kwargs) -> SafeText:
        return render_to_string(
            "widgets/settings_row.html",
            context=self.get_extra_context(input=super().render(**kwargs)),
        )


class SettingsBoolWidget(forms.CheckboxInput, SettingsHelper):
    def __init__(self, **kwargs) -> None:
        kwargs.update({"class": "form-check-input", "autocomplete": "off"})
        super().__init__(self.set_params(**kwargs))

    def render(self, **kwargs) -> SafeText:
        return render_to_string(
            "widgets/settings_row.html",
            context=self.get_extra_context(
                is_checkbox=True, input=super().render(**kwargs)
            ),
        )


FIELDS = {
    bool: (forms.fields.BooleanField, {"required": False}),
    int: (forms.fields.IntegerField, {"widget": forms.TextInput(attrs={"size": 10})}),
    Decimal: (
        forms.fields.DecimalField,
        {"widget": forms.TextInput(attrs={"size": 10})},
    ),
    str: (
        forms.fields.CharField,
        {
            # "widget": SettingsWidget(attrs={"size": 50}),
            "required": False,
        },
    ),
    datetime: (forms.fields.SplitDateTimeField, {"widget": forms.SplitDateTimeWidget}),
    timedelta: (forms.fields.DurationField, {"widget": forms.TextInput}),
    date: (forms.fields.DateField, {"widget": forms.DateInput}),
    time: (forms.fields.TimeField, {"widget": forms.TimeInput}),
    float: (forms.fields.FloatField, {"widget": forms.TextInput(attrs={"size": 10})}),
}


class SettingsForm(forms.Form):
    version = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, initial, request=None, *args, **kwargs):
        super().__init__(*args, initial=initial, **kwargs)
        version_hash = sha256()

        for name, options in settings.CONFIG.items():
            default = options[0]
            config_type = type(default)

            if isinstance(default, str):
                self.fields[name] = forms.fields.CharField(
                    widget=SettingsCharWidget(
                        name=name,
                        default=default,
                        help_text=options[1],
                    )
                )
            elif isinstance(default, bool):
                self.fields[name] = forms.fields.BooleanField(
                    required=False,
                    widget=SettingsBoolWidget(
                        name=name, default=default, help_text=options[1]
                    ),
                )
            elif isinstance(default, int):
                self.fields[name] = forms.fields.IntegerField(
                    widget=SettingsCharWidget(
                        name=name, default=default, help_text=options[1]
                    )
                )
            else:
                field_class, kwargs = FIELDS[config_type]

                self.fields[name] = field_class(label=name, **kwargs)

            self.initial[name] = getattr(config, name)

        self.initial["version"] = version_hash.hexdigest()

    def save(self):
        for name in settings.CONFIG:
            current = getattr(config, name)
            new = self.cleaned_data[name]

            if isinstance(new, str):
                new = normalize_newlines(new)

            if (
                conf.settings.USE_TZ
                and isinstance(current, datetime)
                and not timezone.is_aware(current)
            ):
                current = timezone.make_aware(current)

            if current != new:
                setattr(config, name, new)
