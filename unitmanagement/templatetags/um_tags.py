from django import template
register = template.Library()


@register.filter
def list_item(List, i):

    return List[i]

@register.filter
def formset_item(formset, i):

    return formset.forms[i].fields['quantity']