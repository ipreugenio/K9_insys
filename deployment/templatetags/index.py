from django import template
from deployment.models import Incidents, K9_Schedule
from datetime import date as dt
from django.db.models import Q
from dateutil import parser

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

@register.filter
def days_before_next_request(K9, i):

    schedule = K9_Schedule.objects.filter(Q(k9=K9.id) & Q(date_start__gt=dt.today())).order_by('date_start')

    if schedule:
        days_before = schedule[0].date_start - dt.today()
        days_before = str(days_before.days) + "days"
    else:
        days_before = "No Upcoming Schedule"

    return days_before