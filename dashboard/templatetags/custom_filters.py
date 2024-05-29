from django import template

register = template.Library()

@register.filter
def div(value, arg):
    try:
        return round(value / arg * 100)
    except (ValueError, ZeroDivisionError):
        return None