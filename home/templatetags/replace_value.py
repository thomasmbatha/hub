from django import template

register = template.Library()


@register.filter(name="replace_value")
def replace_value(value, arg):
    """
    Replaces a given value with space and converts to title case
    Example: "hello_world" → "Hello World"
    """

    if not isinstance(value, str):
        return value  # prevent errors

    return value.replace(arg, " ").title()