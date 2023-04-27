import base64

from django import template

register = template.Library()


@register.filter(name='my_filters')
def base64_encode(value):
    return base64.b64encode(value).decode('utf-8')
