from django import template
import html

register = template.Library()

@register.filter
def remove_html_entities(value):
    return html.unescape(value)