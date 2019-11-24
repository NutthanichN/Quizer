from django import template

register = template.Library()


@register.filter
def mul(value, arg):
    """Multiply value and argument"""
    value = int(value)
    arg = int(arg)
    return value * arg


@register.filter(name='times')
def times(number):
    return range(number)
