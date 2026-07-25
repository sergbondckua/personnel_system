from django import template

register = template.Library()


@register.filter
def get_item(sequence, index):
    try:
        return sequence[index]
    except Exception:
        return None
