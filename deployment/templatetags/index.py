from django import template
from deployment.models import Incidents

register = template.Library()

@register.filter
def capability(List, i):
    item = List[int(i)]
    capability = item.capability

    return capability

@register.filter
def incident_count(Location, i):

    incident_count=Incidents.objects.filter(location = Location).count()

    return incident_count