from django import template
from deployment.models import Incidents, K9_Schedule, Team_Dog_Deployed, Team_Assignment, Location, Dog_Request
from datetime import date as dt
from django.db.models import Q
from dateutil import parser
#GeoDjango
from math import sin, cos, radians, degrees, acos
from django.contrib.gis.gdal import SpatialReference, CoordTransform
import math
import ast
from decimal import *
from django.contrib.gis.geos import Point
from pyproj import Proj, transform


register = template.Library()

@register.filter
def get_duration(schedule, i):

    #k9_schedule = K9_Schedule.objects.get(id = i)
    dog_request = Dog_Request.objects.get(id = schedule.dog_request.id)
    duration = dog_request.duration

    return duration

@register.filter
def capability(List, i):
    item = List[int(i)]
    capability = item.capability

    return capability

@register.filter
def incident_count_location(Location, id):

    incident_count=Incidents.objects.filter(location = Location).count()

    return incident_count

@register.filter
def incident_count(K9, request_id):
    incident_count = 0

    try:
        team_dog_deployed = Team_Dog_Deployed.objects.filter(k9=K9).latest('id')
        if (team_dog_deployed.date_pulled is None):
            team_assignment_id = team_dog_deployed.team_assignment.id
            team_assignment = Team_Assignment.objects.get(id=team_assignment_id)
            location = team_assignment.location
            incident_count = Incidents.objects.filter(location=location).count()
            print("TEAM DOG DEPLOYED ID")
            print(team_dog_deployed.id)
    except:
        ...

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

#This method uses the Harvesines formula to calculate distances between 2 coordinates
def calc_dist(long_a, lat_a, long_b, lat_b):
    lat_a = radians(lat_a)
    lat_b = radians(lat_b)
    long_diff = radians(long_a - long_b)
    distance = (sin(lat_a) * sin(lat_b) +
                cos(lat_a) * cos(lat_b) * cos(long_diff))
    resToMile = degrees(acos(distance)) * 69.09
    resToMt = resToMile / 0.00062137119223733
    return resToMile #Return value in Miles

def convert_to_geographic(lon, lat):
    coordinates = []

    inProj = Proj(init='epsg:3857')
    outProj = Proj(init='epsg:4326')
    x1, y1 = lon, lat#-11705274.6374, 4826473.6922
    x2, y2 = transform(inProj, outProj, x1, y1)

    coordinates.append(Decimal(x2))
    coordinates.append(Decimal(y2))

    return coordinates


@register.filter
def calculate_distance_from_current(K9, request_id):
    #calculate distance from current location to request location

    deployed = 0
    pcg_lon = 13476918.53413876
    pcg_lat = 1632299.5848436863

    current_coordinates = convert_to_geographic(pcg_lon, pcg_lat)

    try:
        team_dog_deployed = Team_Dog_Deployed.objects.filter(k9 = K9).latest('id')

        if(team_dog_deployed.date_pulled is None):
            team_assignment_id = team_dog_deployed.team_assignment.id
            team_assignment = Team_Assignment.objects.get(id = team_assignment_id)
            location = team_assignment.location
            print("TEAM DOG DEPLOYED ID")
            print(team_dog_deployed.id)
            current_coordinates = convert_to_geographic(location.longtitude, location.latitude)
            deployed = 1
    except:
        ...
    request = Dog_Request.objects.get(id = request_id)
    target_coordinates = convert_to_geographic(request.longtitude, request.latitude)

    if deployed == 1:
        distance = calc_dist(current_coordinates[0], current_coordinates[1], target_coordinates[0], target_coordinates[1])
    else:
        distance = calc_dist(current_coordinates[0], current_coordinates[1], target_coordinates[0], target_coordinates[1])

    if deployed == 1:
        print(location)
    else:
        print("PCG TAGUIG BASE")
    print(request)
    print("Current Coordinates")
    print(current_coordinates)
    print("Target Coordinates")
    print(target_coordinates)

    return round(distance, 4)

@register.filter
def calculate_distance_from_current_team(K9, team_id):
    #calculate distance from current location to request location

    deployed = 0
    pcg_lon = 13476918.53413876
    pcg_lat = 1632299.5848436863

    current_coordinates = convert_to_geographic(pcg_lon, pcg_lat)

    try:
        team_dog_deployed = Team_Dog_Deployed.objects.filter(k9 = K9).latest('id')

        if(team_dog_deployed.date_pulled is None):
            team_assignment_id = team_dog_deployed.team_assignment.id
            team_assignment = Team_Assignment.objects.get(id = team_assignment_id)
            location = team_assignment.location
            print("TEAM DOG DEPLOYED ID")
            print(team_dog_deployed.id)
            current_coordinates = convert_to_geographic(location.longtitude, location.latitude)
            deployed = 1
        else:
            pass
    except:
        pass

    team = Team_Assignment.objects.get(id = team_id)
    team_location = team.location
    target_coordinates = convert_to_geographic(team_location.longtitude, team_location.latitude)

    if deployed == 1:
        distance = calc_dist(current_coordinates[0], current_coordinates[1], target_coordinates[0], target_coordinates[1])
    else:
        distance = calc_dist(current_coordinates[0], current_coordinates[1], target_coordinates[0], target_coordinates[1])

    print("Current Coordinates")
    print(current_coordinates)
    print("Target Coordinates")
    print(target_coordinates)

    return round(distance, 4)

#TODO Get location for K9s deployed in requests
@register.filter
def current_location(K9, request_id):
    try:
        team_dog_deployed = Team_Dog_Deployed.objects.filter(k9=K9).latest('id')
        print("NOT NONE TEAM DOG DEPLOYED")
        print(team_dog_deployed.__dict__)


        if (team_dog_deployed.date_pulled is None):
            team_assignment_id = team_dog_deployed.team_assignment.id
            team_assignment = Team_Assignment.objects.get(id=team_assignment_id)
            location = team_assignment.location
        else:
            location = "PCGK9 Taguig Base"

    except:
        location = "PCGK9 Taguig Base"

    return location

@register.filter
def current_team(K9, request_id):
    team_dog_deployed = Team_Dog_Deployed.objects.filter(k9=K9).latest('id')
    team_assignment = None

    if (team_dog_deployed.date_pulled is not None):
        team_assignment_id = team_dog_deployed.team_assignment.id
        team_assignment = Team_Assignment.objects.get(id=team_assignment_id)

    return team_assignment