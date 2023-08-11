from django import template

from django.utils.html import format_html
from django.conf import settings

register = template.Library()


@register.simple_tag
def bootstrap():
    return format_html(
        f'<link rel="stylesheet" href="{settings.STATIC_URL}bootstrap/css/bootstrap.min.css">\n<script src="{settings.STATIC_URL}bootstrap/js/bootstrap.min.js"></script>'
    )
    pass


@register.simple_tag
def htmx():
    return format_html(f'<script src="{settings.STATIC_URL}gui/htmx.min.js"></script>')


@register.simple_tag
def jquery():
    return format_html(
        f'<script src="{settings.STATIC_URL}gui/jquery-3.7.0.js"></script>'
    )


@register.simple_tag
def hyperscript():
    return format_html(
        f'<script src="https://unpkg.com/hyperscript.org@0.9.7"></script>'
    )


@register.simple_tag
def gui():
    return format_html(f'<script src="{settings.STATIC_URL}gui/gui.js"></script>')


@register.filter
def get_class_name(value):
    return value.__class__.__name__.lower()
