from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def currency(value):
    try:
        return f'${float(value):,.0f}'
    except (ValueError, TypeError):
        return value


@register.filter
def star_rating(value):
    try:
        n = int(value)
        return mark_safe('★' * n + '☆' * (5 - n))
    except (ValueError, TypeError):
        return ''


@register.simple_tag
def active_nav(request, url_name):
    from django.urls import reverse
    try:
        return 'nav-active' if request.path == reverse(url_name) else ''
    except Exception:
        return ''


@register.inclusion_tag('restaurant/partials/menu_item.html')
def render_menu_item(item):
    return {'item': item}


@register.filter
def truncate_words_html(value, arg):
    """Truncate to arg words, stripping HTML."""
    import re
    text = re.sub(r'<[^>]+>', '', str(value))
    words = text.split()
    if len(words) <= int(arg):
        return text
    return ' '.join(words[:int(arg)]) + '…'
