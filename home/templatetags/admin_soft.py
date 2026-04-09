# hub/home/templatetags/admin_soft.py

import re
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.admin.views.main import PAGE_VAR

# Import from utils.py (your helper functions)
from .utils import get_menu_items  

register = template.Library()


# ======================
# 🔹 FILTERS
# ======================

@register.filter
def clean_text(value):
    """Remove newlines from text."""
    if not isinstance(value, str):
        return value
    return value.replace('\n', ' ')


@register.filter
def checkbox(value):
    """Remove <td> tags from HTML content."""
    if not isinstance(value, str):
        return value
    return re.sub(r"</?(?i:td)(.|\n)*?>", "", value)


@register.filter
def sum_number(value, number):
    """Add two numbers."""
    try:
        return value + number
    except Exception:
        return value


@register.filter
def neg_num(value, number):
    """Subtract numbers."""
    try:
        return value - number
    except Exception:
        return value


# ======================
# 🔹 SIMPLE TAGS
# ======================

@register.simple_tag(takes_context=True)
def admin_get_menu(context):
    """Return admin sidebar menu items."""
    return get_menu_items(context)


@register.simple_tag(takes_context=True)
def get_direction(context):
    """
    Handle RTL (right-to-left) languages like Arabic
    """
    res = {
        'panel': 'text-left',
        'notify': 'right',
        'float': 'float-end',   # ✅ modern bootstrap (was float-right)
        'reverse_panel': 'text-right',
        'nav': 'ms-auto'        # ✅ modern bootstrap (was ml-auto)
    }

    if context.get('LANGUAGE_BIDI'):
        res.update({
            'panel': 'text-right',
            'notify': 'left',
            'float': '',
            'reverse_panel': 'text-left',
            'nav': 'me-auto'    # ✅ modern bootstrap (was mr-auto)
        })

    return res


@register.simple_tag(takes_context=True)
def get_admin_setting(context):
    """
    Placeholder for admin user settings
    (currently not used)
    """
    return {}


@register.simple_tag
def paginator_number(cl, i):
    """
    Custom pagination button for Django admin
    """

    if i == cl.paginator.ELLIPSIS:
        return format_html('{} ', cl.paginator.ELLIPSIS)

    elif i == cl.page_num:
        return format_html(
            '<a href="" class="page-link active">{}</a> ',
            i
        )

    return format_html(
        '<a href="{}" class="page-link {}">{}</a> ',
        cl.get_query_string({PAGE_VAR: i}),
        mark_safe('end' if i == cl.paginator.num_pages else ''),
        i,
    )