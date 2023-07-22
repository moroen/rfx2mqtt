from typing import Any, Mapping, Optional, Type, Union
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
        self, *fields, css_id=None, css_class=None, template=None, width=3, **kwargs
    ):
        if css_class is None:
            css_class = f"col-md-{width}"
        super().__init__(
            *fields, css_id=css_id, css_class=css_class, template=template, **kwargs
        )


class DefaultFormHelper(FormHelper):
    def layout_if(condition):
        if condition:
            return
        else:
            return ()

    def __init__(self, form=None, form_mode=None, devicetype=None):
        super().__init__(form)

        print("Helper", devicetype)

        self.form_method = "post"
        self.form_class = "m-3"
        # self.label_class = "col-sm-2 col-form-label"
        # self.field_class = "col-2"

        fields_layout = Layout(
            Row(
                Column(FloatingField("name")),
                Column(FloatingField("room")),
            ),
            Row(
                Column(FloatingField("ident"), width=2),
                Column(FloatingField("unit"), width=1),
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
                        Column(Field("state")),
                        Column(FloatingField("brightness")),
                    ),
                )
            else:
                state_layout = Layout(
                    Row(
                        Column(Field("state")),
                    )
                )

        else:
            state_layout = Layout()

        if "temp" in form.fields:
            temp_layout = Layout(
                Row(
                    Column(FloatingField("temp"), width=1),
                    Column(FloatingField("humidity"), width=2),
                ),
            )
        else:
            temp_layout = Layout()

        if form_mode == "update":
            button_layout = Layout(
                Row(
                    Column(
                        Submit(name="Submit", value="Save", css_class="btn-primary")
                    ),
                    Column(
                        HTML(
                            '<button hx-get="{% url \'device-delete\' pk=object.id%}" hx-target="#modals-here" hx-trigger="click" _="on htmx:afterOnLoad wait 10ms then add .show to #modal then add .show to #modal-backdrop" class="btn btn-danger">Delete</button>'
                        )
                    ),
                )
            )
        elif form_mode == "add":
            button_layout = Layout(
                Row(
                    Column(
                        Submit(name="Submit", value="Save", css_class="btn-primary")
                    ),
                    Column(
                        HTML(
                            '<button hx-get="{% url \'device-list\' %}" hx-target="#whole" hx-trigger="click" _="on htmx:afterOnLoad wait 10ms then add .show to #modal then add .show to #modal-backdrop" class="btn btn-danger">Cancel</button>'
                        )
                    ),
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
