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

from crispy_bootstrap5.bootstrap5 import FloatingField
from django.template.loader import render_to_string
from django.urls import reverse_lazy


class Column(Column):
    def __init__(
        self, *fields, css_id=None, css_class=None, template=None, width=6, **kwargs
    ):
        if css_class is None:
            css_class = f"col-md-{width}"
        super().__init__(
            *fields, css_id=css_id, css_class=css_class, template=template, **kwargs
        )


class RoomFormHelper(FormHelper):
    def __init__(self, form=None, target=None):
        super().__init__(form)
        self.form_class = "m-3"
        if target is not None:
            self.form_action = target

        self.layout = Layout(
            Row(Column(FloatingField("name", autofocus="autofocus"))),
            Row(
                Column(Submit(name="Submit", value="Save", css_class="btn-primary")),
                Column(HTML(render_to_string("widgets/close_button.html"))),
            ),
        )
