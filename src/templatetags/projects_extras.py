import markdown
from django import template

register = template.Library()


@register.filter
def convert_markdown(value):
    return markdown.markdown(
        value,
        extensions=[
            "markdown.extensions.fenced_code",
            "markdown.extensions.wikilinks",
        ],
    )
