from typing import Any, Mapping, Optional, Type, Union
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Layout,
    Div,
    Submit,
    HTML,
    Button,
    Row,
    Field,
    Column,
    Hidden,
)

# from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, InlineField
from crispy_bootstrap5.bootstrap5 import FloatingField

from crispy_forms.layout import Field, Button, Submit


class Column(Column):
    def __init__(
        self, *fields, css_id=None, css_class=None, template=None, width=6, **kwargs
    ):
        if css_class is None:
            css_class = f"col-md-{width}"
        super().__init__(
            *fields, css_id=css_id, css_class=css_class, template=template, **kwargs
        )


class Switch(Field):
    def __init__(
        self, *fields, css_class=None, wrapper_class=None, template=None, **kwargs
    ):
        wrapper_class = (
            wrapper_class if wrapper_class is not None else "form-check form-switch"
        )
        css_class = css_class if css_class is not None else "form-check-input"
        super().__init__(
            *fields,
            css_class=css_class,
            wrapper_class=wrapper_class,
            template=template,
            **kwargs,
        )


class DeviceFormHelper(FormHelper):
    def __init__(self, form=None, form_mode=None, devicetype=None):
        super().__init__(form)

        self.form_method = "post"
        self.form_class = "m-3"

        fields_layout = Layout(
            Row(
                Column(FloatingField("name", autofocus="autofocus")),
                Column(FloatingField("room")),
                Column(Switch("mqtt_discover")),
            ),
            Row(
                Column(FloatingField("ident"), width=4),
                Column(FloatingField("unit"), width=2),
            ),
            Row(
                Column(FloatingField("packet_type")),
                Column(FloatingField("device_protocol")),
            ),
        )

        if "state" in form.fields:
            if "brightness" in form.fields:
                state_layout = Layout(
                    Row(
                        Column(Switch("state")),
                        Column(FloatingField("brightness")),
                    ),
                )
            else:
                state_layout = Layout(
                    Row(
                        Column(Switch("state")),
                    )
                )

        else:
            state_layout = Layout()

        if "temp" in form.fields:
            temp_layout = Layout(
                Row(
                    Column(FloatingField("temp"), width=3),
                    Column(FloatingField("humidity"), width=3),
                ),
            )
        else:
            temp_layout = Layout()

        if form_mode == "update":
            button_layout = Layout(
                Row(
                    Column(
                        Submit(name="Submit", value="Save", css_class="btn-primary"),
                        width=2,
                    ),
                    Column(
                        HTML(
                            '<button hx-get="{% url \'DEVICES:delete\' pk=object.id%}" hx-target="#modals-here" hx-trigger="click" _="on htmx:afterOnLoad wait 10ms then add .show to #modal then add .show to #modal-backdrop" class="btn btn-danger">Delete</button>'
                        ),
                        width=6,
                    ),
                    Column(
                        HTML(render_to_string("widgets/close_button.html")), width=2
                    ),
                )
            )
        elif form_mode == "add":
            self.form_action = reverse_lazy("DEVICES:add")
            button_layout = Layout(
                Row(
                    Column(
                        Submit(name="Submit", value="Save", css_class="btn-primary")
                    ),
                    Column(HTML(render_to_string("widgets/close_button.html"))),
                )
            )
        else:
            button_layout = Layout()

        if devicetype is not None:
            print("Helper 2", devicetype)
            fields_layout = Layout(
                Hidden("devicetype", value=devicetype), fields_layout
            )

        self.layout = Layout(fields_layout, state_layout, temp_layout, button_layout)
