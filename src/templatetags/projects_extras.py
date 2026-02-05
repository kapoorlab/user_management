import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def convert_markdown(value):
    if not value:
        return ""
    html = markdown.markdown(
        value,
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.nl2br",
            "markdown.extensions.sane_lists",
            "markdown.extensions.codehilite",
        ],
    )
    return mark_safe(html)
