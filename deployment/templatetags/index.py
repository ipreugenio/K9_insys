from django import template

register = template.Library()

@register.filter
def capability(List, i):
    item = List[int(i)]
    capability = item.capability

    return capability