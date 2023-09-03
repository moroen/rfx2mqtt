from django.template.loader import render_to_string
from typing import Any, Dict


class FilterBoxMixin:
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {"functionbar_left": render_to_string("widgets/hx_filter_box.html")}
        )
        return context


class AddButtonMixin:
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "functionbar_right": render_to_string(
                    "widgets/hx_popup_button.html",
                    {
                        "label": self.add_button_label,
                        "target": self.add_button_target,
                        "button_class": self.add_button_class,
                    },
                ),
            }
        )
        return context
