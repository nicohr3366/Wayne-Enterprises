from django import template

register = template.Library()


@register.filter
def url_tail(value):
    if not value:
        return ''
    return value.split(':')[-1]
