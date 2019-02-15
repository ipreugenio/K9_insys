from django import template
register = template.Library()


@register.filter
def list_item(List, i):

    return List[i]