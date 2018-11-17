from django import template
register = template.Library()


@register.filter
def skill_score(List, i):
    if List[i] == List[-1]:
        result = "Recommended!"
    else:
        result = ""

    return result