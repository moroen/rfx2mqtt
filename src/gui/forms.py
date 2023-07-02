from typing import Any, Dict, Mapping, Optional, Type, Union
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from api.models import Device, Switch
from django.forms.utils import ErrorList

from polymorphic.formsets import (
    polymorphic_modelformset_factory,
    PolymorphicFormSetChild,
)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class DefaultFormHelper(FormHelper):
    def __init__(self, form=None):
        super().__init__(form)

        self.form_method = "post"
        self.attrs = {"class": "ms-3 me-3"}
        self.add_input(Submit("submit", "Save"))


class DeviceForm(ModelForm):
    class Meta:
        model = Switch
        fields = "__all__"

    def __init__(self, *args, **kwargs) -> None:
        super(DeviceForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_method = "post"
        self.helper.attrs = {"class": "ms-3"}

    # helper = FormHelper()
    # helper.form_class = "form-horizontal"
    # helper.layout = Layout(
    #     Field("text_input", css_class="input-xlarge"),
    #     Field("textarea", rows="3", css_class="input-xlarge"),
    #     "radio_buttons",
    #     Field("checkboxes", style="background: #FAFAFA; padding: 10px;"),
    #     AppendedText("appended_text", ".00"),
    #     PrependedText(
    #         "prepended_text",
    #         '<input type="checkbox" checked="checked" value="" id="" name="">',
    #         active=True,
    #     ),
    #     PrependedText("prepended_text_two", "@"),
    #     "multicolon_select",
    #     FormActions(
    #         Submit("save_changes", "Save changes", css_class="btn-primary"),
    #         Submit("cancel", "Cancel"),
    #     ),
    # )
