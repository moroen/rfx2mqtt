from django import template

from django.utils.html import format_html
from django.conf import settings


register = template.Library()


@register.simple_tag
def device_type(object):
    return object.__class__.__name__.lower()
