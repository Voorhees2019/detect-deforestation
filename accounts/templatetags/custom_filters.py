from django import template

register = template.Library()


@register.filter
def normalize_table_number(value, arg):
    return value + 10 * (arg - 1)
