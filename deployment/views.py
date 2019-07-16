from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages

from django.db.models import Count
from django.db.models import Q
from django.views import generic
from django.utils.safestring import mark_safe
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from pandas import DataFrame as df
import pandas as pd

import datetime
import re
import sys
from datetime import date

from unitmanagement.models import Notification
from training.models import K9_Handler
from planningandacquiring.models import K9
from profiles.models import Personal_Info, User, Account
from inventory.models import Medicine

from deployment.forms import AreaForm, LocationForm, AssignTeamForm, EditTeamForm, RequestForm, IncidentForm, GeoForm, MonthYearForm, GeoSearch, DateForm, SelectLocationForm

from deployment.models import Area, Location, Team_Assignment, Team_Dog_Deployed, Dog_Request, K9_Schedule, Incidents, Daily_Refresher, Maritime, TempDeployment, K9_Pre_Deployment_Items
from deployment.forms import AreaForm, LocationForm, AssignTeamForm, EditTeamForm, RequestForm, IncidentForm, DailyRefresherForm, ScheduleUnitsForm, DeploymentDateForm

from pyproj import Proj, transform

#Plotly
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.graph_objs.layout as lout
import plotly.figure_factory as ff

#GeoDjango
from math import sin, cos, radians, degrees, acos
import math
import ast
from decimal import *

import datetime
from datetime import timedelta, date

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe

from deployment.util import Calendar, get_date, prev_month, next_month, select_month, Calendar_Detailed
from collections import OrderedDict
import json

from deployment.templatetags import index as deployment_template_tags



class MyDictionary(dict):

    # __init__ function
    def __init__(self):
        self = dict()

        # Function to add key:value

    def add(self, key, value):
        self[key] = value

def notif(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)
    
    if user_in_session.position == 'Veterinarian':
        notif = Notification.objects.filter(position='Veterinarian').order_by('-datetime')
    elif user_in_session.position == 'Handler':
        notif = Notification.objects.filter(user=user_in_session).order_by('-datetime')
    else:
        notif = Notification.objects.filter(position='Administrator').order_by('-datetime')
   
    return notif


def user_session(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)
    return user_in_session

def index(request):
    d = Daily_Refresher.objects.get(id=4)

    context = {
      'title':'Deployment',
      'd':d,
    }
    return render (request, 'deployment/index.html', context)

def add_area(request):
    form = AreaForm(request.POST or None)
    style = ""
    area = None
    if request.method == 'POST':
        if form.is_valid():
            area = form.save()
            style = "ui green message"
            messages.success(request, 'Area has been successfully Added!')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
      'title':'Add Area Form',
      'texthelp': 'Input Name of Area Here',
      'form': form,
      'actiontype': 'Submit',
      'style':style,
      'notif_data':notif_data,
      'count':count,
      'user':user,
    }
    return render (request, 'deployment/add_area.html', context)

def add_location(request):
    form = LocationForm(request.POST or None)

    geoform = GeoForm(request.POST or None)
    geosearch = GeoSearch(request.POST or None)
    width = 470
    style = ""

    if request.method == 'POST':
        print(form.errors)
        if form.is_valid() and geoform.is_valid():
            location = form.save()

            team = Team_Assignment.objects.create(location = location)
            team.save()

            checks = geoform['point'].value()
            checked = ast.literal_eval(checks)
            print(checked['coordinates'])
            toList = list(checked['coordinates'])
            print(toList)
            lon = Decimal(toList[0])
            lat = Decimal(toList[1])
            print("LONGTITUDE")
            print(lon)
            print("LATITUDE")
            print(lat)
            location.longtitude = lon
            location.latitude = lat
            location.save()

            style = "ui green message"
            messages.success(request, 'Location has been successfully Added!')
            form = LocationForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
      'title':'Add Location Form',
      'texthelp': 'Input Location Details Here',
      'form': form,
      'geoform': geoform,
      'geosearch': geosearch,
       'width' :width,

      'actiontype': 'Submit',
      'style':style,
      'notif_data':notif_data,
      'count':count,
      'user':user,

    }
    return render (request, 'deployment/add_location.html', context)


def load_locations(request):

    search_query = request.GET.get('search_query')
    width = request.GET.get('width')


    if search_query == "":
        geolocator = Nominatim(user_agent="Locator", timeout=None)
    else:
        geolocator = Nominatim(user_agent="Locator", format_string="%s, Philippines", timeout=None)

    locations = geolocator.geocode(search_query, exactly_one=False)

    print(locations)

    context = {
        'locations' : locations,
        'width': width
    }

    return render(request, 'deployment/location_data.html', context)

def load_map(request):
    lng = request.GET.get('lng')
    lat = request.GET.get('lat')

    width = request.GET.get('width')

    print("TEST coordinates")
    print(str(lat) + " , " + str(lng))

    geoform = GeoForm(request.POST or None, lat=lat, lng=lng, width=width)

    context = {
        'geoform' : geoform
    }

    return render(request, 'deployment/map_data.html', context)

def assign_team_location(request):
    form = AssignTeamForm(request.POST or None)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            f = form.save(commit=False)
            f.team_leader.assigned=True
            f.location.status='assigned'
            f.save()

            print(f)

            style = "ui green message"
            messages.success(request, 'Location has been successfully Added!')
            form = AssignTeamForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
      'title':'Assign Team to Location',
      'texthelp': 'Input Team and Location Details Here',
      'form': form,
      'actiontype': 'Submit',
      'style':style,
      'notif_data':notif_data,
      'count':count,
      'user':user,
    }
    return render (request, 'deployment/assign_team_location.html', context)

def edit_team(request, id):
    data = Team_Assignment.objects.get(id=id)
    form = EditTeamForm(request.POST or None, instance = data)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            data.team = request.POST.get('team')
            data.EDD_demand = request.POST.get('EDD_demand')
            data.NDD_demand = request.POST.get('NDD_demand')
            data.SAR_demand = request.POST.get('SAR_demand')
            data.save()
            style = "ui green message"
            messages.success(request, 'Team Details has been successfully Updated !')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
      'title': data.team,
      'texthelp': 'Edit Team Details Here',
      'form': form,
      'data': data,
      'actiontype': 'Submit',
      'style':style,
      'notif_data':notif_data,
      'count':count,
      'user':user,
    }
    return render(request, 'deployment/edit_team.html', context)

def assigned_location_list(request):
    data = Team_Assignment.objects.all()

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title' : 'DOGS AND HANDLERS ASSIGNED FOUs',
        'data' : data,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'deployment/assigned_location_list.html', context)

def team_location_details(request, id):
    data = Team_Assignment.objects.get(id=id)
    incidents = Incidents.objects.filter(location = data.location)
    edd_inc = Incidents.objects.filter(location = data.location).filter(type = "Explosives Related").count()
    ndd_inc = Incidents.objects.filter(location=data.location).filter(type="Narcotics Related").count()
    sar_inc = Incidents.objects.filter(location=data.location).filter(type="Search and Rescue Related").count()
    style = ""

    #filter personal_info where city != Team_Assignment.city
    handlers = Personal_Info.objects.exclude(city=data.location.city)
    
    user_deploy = [] 
    for h in handlers:
       user_deploy.append(h.UserID)

    # #filter K9 where handler = person_info and k9 assignment = None
    can_deploy = K9.objects.filter(handler__in=user_deploy).filter(training_status='For-Deployment').filter(assignment='None')
    
    dogs_deployed = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(status='Deployed')
    dogs_pulled = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(status='Pulled-Out')
  

    if request.method == 'POST':
        checks =  request.POST.getlist('checks') # get the id of all the dogs checked
        #print(checks)

        #get the k9 instance of checked dogs
        checked_dogs = K9.objects.filter(id__in=checks)
        #print(checked_dogs)

        for checked_dogs in checked_dogs:
            Team_Dog_Deployed.objects.create(team_assignment=data, k9=checked_dogs) # date = team_assignment
            # TODO: if dog is equal capability increment
            if checked_dogs.capability == 'EDD':
                data.EDD_deployed = data.EDD_deployed + 1
            elif checked_dogs.capability == 'NDD':
                data.NDD_deployed = data.NDD_deployed + 1
            else:
                data.SAR_deployed = data.SAR_deployed + 1

            data.save()
            dog = K9.objects.get(id=checked_dogs.id)
            dog.assignment = str(data)
            dog.save()

        messages.success(request, 'Dogs has been successfully Deployed!')

        return redirect('deployment:team_location_details', id = id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title' : data,
        'data' : data,
        'style': style,
        'can_deploy':can_deploy,
        'dogs_deployed':dogs_deployed,
        'dogs_pulled': dogs_pulled,
        'sar_inc': sar_inc,
        'ndd_inc': ndd_inc,
        'edd_inc': edd_inc,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'deployment/team_location_details.html', context)

def remove_dog_deployed(request, id):
    pull_k9 = Team_Dog_Deployed.objects.get(id=id)
    k9 = K9.objects.get(id=pull_k9.k9.id)
    team_assignment = Team_Assignment.objects.get(id=pull_k9.team_assignment.id)

    #change Team_Dog_Deployed model
    pull_k9.status = 'Pulled-Out'
    pull_k9.date_pulled = datetime.date.today()
    pull_k9.save()

    #change K9 model
    k9.assignment = 'None'
    k9.save()

    #change Team_Assignment model
    if pull_k9.k9.capability == 'EDD':
         team_assignment.EDD_deployed  = team_assignment.EDD_deployed - 1
    elif pull_k9.k9.capability == 'NDD':
        team_assignment.NDD_deployed = team_assignment.NDD_deployed - 1
    elif pull_k9.k9.capability == 'SAR':
        team_assignment.SAR_deployed = team_assignment.SAR_deployed - 1
    else:
        pass
    team_assignment.save()

    messages.success(request, 'Dogs has been successfully Pulled!')

    return redirect('deployment:team_location_details', id=pull_k9.team_assignment.id)

def dog_request(request):

    form = RequestForm(request.POST or None)

    geoform = GeoForm(request.POST or None, width=750)
    style = ""
    geosearch = GeoSearch(request.POST or None)
    width = 750

    style = ""

    if request.method == 'POST':
        print(form.errors)
        form.validate_date()
        if form.is_valid():

            cd = form.cleaned_data['phone_number']
            regex = re.compile('[^0-9]')
            form.phone_number = regex.sub('', cd)

            location = form.save() #instance of form

            checks = geoform['point'].value()
            checked = ast.literal_eval(checks)
            print(checked['coordinates'])
            toList = list(checked['coordinates'])
            print(toList)
            lon = Decimal(toList[0])
            lat = Decimal(toList[1])
            print("LONGTITUDE")
            print(lon)
            print("LATITUDE")
            print(lat)
            location.longtitude = lon
            location.latitude = lat

            serial = request.session['session_serial']
            account = Account.objects.get(serial_number=serial)
            user_in_session = User.objects.get(id=account.UserID.id)


            if location.sector_type != "Disaster": #TODO, wala pa process for disasters
                if user_in_session.position == 'Operations' or  user_in_session.position == 'Administrator':
                    location.sector_type = "Big Event"
                    location.status = "Approved"
                else:
                    location.sector_type = "Small Event"


            location.save()

            style = "ui green message"
            messages.success(request, 'Request has been successfully Added!')
            form = RequestForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
      'title':'Request Form',
      'texthelp': 'Input request of client here.',
      'form': form,

      'geoform' : geoform,
       'geosearch' : geosearch,
        'width' : width,

      'actiontype': 'Submit',
      'style':style,
      'notif_data':notif_data,
      'count':count,
      'user':user,
    }
    return render (request, 'deployment/request_form.html', context)

def request_dog_list(request):
    data = Dog_Request.objects.all()

    date_now = datetime.date.today()


    # latest_date = Dog_Request.objects.latest('end_date')
    # latest_date = latest_date.end_date
    # k9_schedule = Dog_Request.objects.filter(end_date__range=[str(date_now), str(latest_date)])

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'data': data,
        'title': 'Request Dog List',
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'deployment/request_dog_list.html', context)

def request_dog_details(request, id):
    data2 = Dog_Request.objects.get(id=id)
    '''data = Team_Assignment.objects.get(id=id)'''
    k9 = Team_Dog_Deployed.objects.filter(team_requested=data2)
    style = ""
    # filter personal_info where city != Team_Assignment.city
    handlers = Personal_Info.objects.exclude(city=data2.city)

    handler_can_deploy = []  # append the id of the handlers
    for h in handlers:
        handler_can_deploy.append(h.id)
    # print(handler_can_deploy)

    # get instance of user using personal_info.id
    # id of user is the fk.id of person_info
    user = User.objects.filter(id__in=handler_can_deploy)
    # print(user)

    user_deploy = []  # append the user itself
    for u in user:
        user_deploy.append(u.id)

    print(user_deploy)
    # #filter K9 where handler = person_info and k9 assignment = None
    can_deploy = K9.objects.filter(handler__id__in=user_deploy).filter(training_status='For-Deployment').filter(
        assignment='None')
    # print(can_deploy)

    # dogs deployed to Dog Request
    dogs_deployed = Team_Dog_Deployed.objects.filter(team_requested=data2).filter(Q(status='Deployed') | Q(status='Scheduled'))

    sar_deployed = 0
    ndd_deployed = 0
    edd_deployed = 0

    for item in dogs_deployed:
        if item.k9.capability == "SAR":
            sar_deployed += 1
        elif item.k9.capability == "NDD":
            ndd_deployed += 1
        else:
            edd_deployed += 1

    #>>>> start of new Code for saving schedules instead of direct deployment
    # TODO Filter can deploy to with teams without date conflicts
    can_deploy_filtered = []
    for k9 in can_deploy:
        #1 = true, 0 = false
        deployable = 1
        schedules = K9_Schedule.objects.filter(k9=k9).filter(status ="Request")
        print("can_deploy")
        print(k9)
        #TODO obtain schedule of request then compare to start and end date of schedules (loop)
        for sched in schedules:
            if (sched.date_start >= data2.start_date and sched.date_start <= data2.end_date) or (sched.date_end >= data2.start_date and sched.date_end <= data2.end_date) or (data2.start_date >= sched.date_start and data2.start_date <= sched.date_end) or (data2.end_date >= sched.date_start and data2.end_date <= sched.date_end):
                deployable = 0

        if deployable == 1 and deployment_template_tags.current_location(k9, data2.id) != "PCGK9 Taguig Base": #checks if K9's current location is at a port
            can_deploy_filtered.append(k9.id)

    can_deploy2 =  K9.objects.filter(id__in = can_deploy_filtered) #Trained and Assigned dogs without date conflicts TODO Remove K9s that have not yet been deployed to a port
    #TODO If a dog is deployed to a request, the dog will only be deployed if system datetime is same as scheduled request.
    #>>Also, dog deployment means scheduling first

    can_deploy = can_deploy2

    #K9s that are within AOR of request
    k9s_within_AOR = []
    if data2.sector_type == "Small Event":
        AOR = data2.area
        for k9 in can_deploy:
            location = deployment_template_tags.current_location(k9, data2.id)
            if location  != "PCGK9 Taguig Base":
                if location.area == AOR:
                    k9s_within_AOR.append(k9.id)


    #TODO Combine df of within AOR and ouside AOR if event is small

    can_deploy_list = []
    maritime_count_list = []
    incident_count_list = [] #Note: only related to skill
    distance_list = [] #distance of current location to request
    location_list =[]
    area_list = []

    if data2.sector_type == "Small Event":
        can_deploy_inside_AOR = can_deploy.filter(pk__in = k9s_within_AOR)
        can_deploy_outside_AOR = can_deploy.exclude(pk__in = k9s_within_AOR)

        can_deploy = can_deploy_inside_AOR #TODO as of this code, only units within AOR if Small Event

    for k9 in can_deploy:
        can_deploy_list.append(k9)
        maritime_count = 0
        incident_count = 0

        try:
            team_dog_deployed = Team_Dog_Deployed.objects.filter(k9=k9, status="Deployed").latest('id')
            if (team_dog_deployed.date_pulled is None):
                team_assignment_id = team_dog_deployed.team_assignment.id
                team_assignment = Team_Assignment.objects.get(id=team_assignment_id)
                location = team_assignment.location
                location_list.append(location)
                area_list.append(location.area)

                maritime_count = Maritime.objects.filter(location=location).count()
                maritime_count_list.append(maritime_count)

                if k9.capability == "SAR":
                    incident_count = Incidents.objects.filter(location=location).filter(
                        type="Search and Rescue Related").count()

                if k9.capability == "NDD":
                    incident_count = Incidents.objects.filter(location=location).filter(
                        type="Narcotics Related").count()
                else:
                    incident_count = Incidents.objects.filter(location=location).filter(
                        type="Explosives Related").count()
                incident_count_list.append(incident_count)

        except:
            location_list.append("PCGK9 Taguig Base")
            area_list.append("National Capital Region")
            maritime_count_list.append(int(0))
            incident_count_list.append(int(0))


        distance = deployment_template_tags.calculate_distance_from_current(k9, data2.id)
        distance_list.append(distance)

    df_data = {
        "K9" : can_deploy_list,
        "Location" : location_list,
        "Area" : area_list,
        "Distance" : distance_list,
        "Maritime" : maritime_count_list,
        "Incident" : incident_count_list,
    }

    #TODO Find a way to somehow put all within AOR on top first for Small Events, otherwise create a seperate dataframe
    can_deploy_dataframe = df(data=df_data)
    can_deploy_dataframe.sort_values(by=["Distance", "Maritime", "Incident"],
                                   ascending=[True, True, True])

    if data2.sector_type == "Small Event":
        for k9 in can_deploy_outside_AOR:
            can_deploy_list.append(k9)
            maritime_count = 0
            incident_count = 0

            try:
                team_dog_deployed = Team_Dog_Deployed.objects.filter(k9=k9, status="Deployed").latest('id')
                if (team_dog_deployed.date_pulled is None):
                    team_assignment_id = team_dog_deployed.team_assignment.id
                    team_assignment = Team_Assignment.objects.get(id=team_assignment_id)
                    location = team_assignment.location
                    location_list.append(location)
                    area_list.append(location.area)

                    maritime_count = Maritime.objects.filter(location=location).count()
                    maritime_count_list.append(maritime_count)

                    if k9.capability == "SAR":
                        incident_count = Incidents.objects.filter(location=location).filter(
                            type="Search and Rescue Related").count()

                    if k9.capability == "NDD":
                        incident_count = Incidents.objects.filter(location=location).filter(
                            type="Narcotics Related").count()
                    else:
                        incident_count = Incidents.objects.filter(location=location).filter(
                            type="Explosives Related").count()
                    incident_count_list.append(incident_count)

            except:
                location_list.append("PCGK9 Taguig Base")
                area_list.append("National Capital Region")
                maritime_count_list.append(int(0))
                incident_count_list.append(int(0))

            distance = deployment_template_tags.calculate_distance_from_current(k9, data2.id)
            distance_list.append(distance)

        df_data = {
            "K9": can_deploy_list,
            "Location": location_list,
            "Area": area_list,
            "Distance": distance_list,
            "Maritime": maritime_count_list,
            "Incident": incident_count_list,
        }

        # TODO Find a way to somehow put all within AOR on top first for Small Events, otherwise create a seperate dataframe
        can_deploy_outside_AOR_dataframe = df(data=df_data)
        can_deploy_outside_AOR_dataframe.sort_values(by=["Distance", "Maritime", "Incident"],
                                         ascending=[True, True, True])

        can_deploy_dataframe = pd.concat([can_deploy_dataframe, can_deploy_outside_AOR_dataframe])
        can_deploy_dataframe.reset_index(drop=True, inplace=True)

    if request.method == 'POST':
        if 'approve' in request.POST:
            data2.remarks = request.POST.get('remarks')
            data2.status = "Approved"
            data2.save()
            return redirect('deployment:request_dog_details', id=id)
        elif 'deny' in request.POST:
            data2.remarks = request.POST.get('remarks')
            data2.status = "Denied"
            data2.save()
            return redirect('deployment:request_dog_details', id=id)

        checks = request.POST.getlist('checks')  # get the id of all the dogs checked
        # print(checks)

        # get the k9 instance of checked dogs
        checked_dogs = K9.objects.filter(id__in=checks)
        # print(checked_dogs)

        for checked_dogs in checked_dogs:
            #TODO automatic approve pag operations (+ admin na rin siguro pero wala naman dapat access admin dito lol)

            Team_Dog_Deployed.objects.create(team_requested=data2, k9=checked_dogs, status="Scheduled", handler = str(k9.handler.fullname)) #TODO Only save k9.assignment when system datetime is same as request
            
            K9_Schedule.objects.create(k9 = checked_dogs, dog_request = data2, date_start = data2.start_date, date_end = data2.end_date, status = "Request")

            # TODO: if dog is equal capability increment
            if checked_dogs.capability == 'EDD':
                data2.EDD_deployed = data2.EDD_deployed + 1
            elif checked_dogs.capability == 'NDD':
                data2.NDD_deployed = data2.NDD_deployed + 1
            else:
                data2.SAR_deployed = data2.SAR_deployed + 1

            data2.save()
            dog = K9.objects.get(id=checked_dogs.id)
            #dog.assignment = str(data2) #TODO remove assignement for dog requests, only do this if schedule is already hit
            #dog.save()

        style = "ui green message"
        messages.success(request, 'Dogs has been successfully Deployed!')

        return redirect('deployment:request_dog_details', id=id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': data2,
        'data2': data2,
        'can_deploy': can_deploy,
        'style': style,
        'dogs_deployed': dogs_deployed,
        'user':user,
        'can_deploy_df': can_deploy_dataframe,

        'sar_deployed' : sar_deployed,
        'ndd_deployed' : ndd_deployed,
        'edd_deployed' : edd_deployed
    }

    return render(request, 'deployment/request_dog_details.html', context)

def remove_dog_request(request, id):
    pull_k9 = Team_Dog_Deployed.objects.get(id=id)
    k9 = K9.objects.get(id=pull_k9.k9.id)
    dog_request = Dog_Request.objects.get(id=pull_k9.team_requested.id)

    sched = K9_Schedule.objects.get(Q(k9 = k9) & Q(dog_request = dog_request))
    sched.delete()

    #change Team_Dog_Deployed model
    pull_k9.status = 'Pulled-Out'
    pull_k9.date_pulled = datetime.date.today()
    pull_k9.save()

    #change K9 model
    k9.assignment = 'None'
    k9.save()
    #TODO Only put None if K9 is currently deployed on said request

    #change Dog_Request model
    if pull_k9.k9.capability == 'EDD':
        dog_request.EDD_deployed  = dog_request.EDD_deployed - 1
    elif pull_k9.k9.capability == 'NDD':
        dog_request.NDD_deployed = dog_request.NDD_deployed - 1
    elif pull_k9.k9.capability == 'SAR':
        dog_request.SAR_deployed = dog_request.SAR_deployed - 1
    else:
        pass
    dog_request.save()

    messages.success(request, 'Dogs has been successfully Pulled!')

    return redirect('deployment:request_dog_details', id=pull_k9.team_requested.id)

# def deployment_report(request):
#     assignment = Team_Assignment.objects.all()
#
#     #NOTIF SHOW
#     notif_data = notif(request)
#     count = notif_data.filter(viewed=False).count()
#     user = user_session(request)
#     context = {
#         'title': 'Request Dog List',
#         'assignment': assignment,
#         'notif_data':notif_data,
#         'count':count,
#         'user':user,
#     }
#     return render (request, 'deployment/request_dog_list.html', context)


def view_schedule(request, id):

    date_now = datetime.date.today()

    k9 = K9.objects.get(id = id)


    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'k9' : k9,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'deployment/k9_schedule.html', context)

def deployment_area_details(request):
    user = user_session(request)

    data = Team_Assignment.objects.get(team_leader=user)

    tdd = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(status='Deployed')
    
    sar_inc = Incidents.objects.filter(location=data.location).filter(type='Search and Rescue Related').count()
    ndd_inc = Incidents.objects.filter(location=data.location).filter(type='Narcotics Related').count()
    edd_inc = Incidents.objects.filter(location=data.location).filter(type='Explosives Related').count()
    incidents = Incidents.objects.filter(location=data.location).filter(type='Others').count()

    mn = []
    for td in tdd:
        pi = Personal_Info.objects.get(UserID=td.handler)
        mn.append(pi.mobile_number)

    data_list = zip(tdd, mn)
    

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data':data,
        'tdd':tdd,
        'sar_inc':sar_inc,
        'ndd_inc':ndd_inc,
        'edd_inc':edd_inc,
        'incidents':incidents,
        'data_list':data_list,
    }

    return render(request, 'deployment/deployment_area_details.html', context)

def add_incident(request):
    user = user_session(request)
    form = IncidentForm(request.POST or None)
    style = "ui green message"


    user_serial = request.session['session_serial']

    print("USER SERIAL")
    print(user_serial)

    user = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user.UserID.id)

    ta = Team_Assignment.objects.get(team_leader=user)


    form.initial['date'] = date.today() 
    form.fields['location'].queryset = Location.objects.filter(id=ta.location.id)
    
    if request.method == 'POST':
        if form.is_valid():
            f = form.save(commit=False)
            f.user = user
            f.save() 

            style = "ui green message"
            messages.success(request, 'Incident has been successfully added!')
            return redirect('deployment:add_incident')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'title': 'Report Incident Form',
        'texthelp': 'Input Incident Details Here',
        'form': form,
        'actiontype': 'Submit',
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render(request, 'deployment/incident_form.html', context)

def incident_list(request):
    title = "Incidents List View"
    incidents = Incidents.objects.all()

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'incidents': incidents,
        'title': title,
        'notif_data':notif_data,
        'count':count,
        'user':user,        
    }

    return render(request, 'deployment/incident_list.html', context)


def choose_date(request):
    form = DateForm(request.POST or None)

def fou_details(request):
    user = user_session(request)
    data = Team_Assignment.objects.get(team_leader=user)

    tdd = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(status='Deployed')
    
    a = []
    for td in tdd:
        a.append(td.handler)

    #a =User.objects.filter(id=tdd.handler.id)
    pi = Personal_Info.objects.filter(UserID__in = a)

    data_list = zip(tdd,pi)
   
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data_list':data_list,
    }

    return render(request, 'deployment/fou_details.html', context)

def daily_refresher_form(request):
    user = user_session(request)
    k9 = K9.objects.get(handler=user)
    form = DailyRefresherForm(request.POST or None)
    style = "ui green message"
    drf = Daily_Refresher.objects.filter(handler=user).filter(date=datetime.date.today())
    
    dr = None
    if drf.exists():
        dr = 1
    else:
        dr = 0

    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            f = form.save(commit=False)
            f.k9 = k9
            f.handler = user

            mar = request.POST.get('select')
            f.mar = mar
            #TODO Formula for Rating
            port = (f.port_find / f.port_plant * 20)
            building = (f.building_find /f.building_plant * 20)
            vehicle = (f.vehicle_find /f.vehicle_plant * 20)
            baggage = (f.baggage_find /f.baggage_plant * 20)
            others = (f.others_find /f.others_plant * 20)
            find = (f.port_find+f.building_find+f.vehicle_find+f.baggage_find+f.others_find)
            plant = (f.port_plant+f.building_plant+f.vehicle_plant+f.baggage_plant+f.others_plant)

            f.rating = 100 - ((plant - find) * 5)

            #TIME
            #time = (f.port_time + f.building_time + f.vehicle_time + f.baggage_time + f.others_time)
            print(f.port_time)
            ######################
            f.save()
            
            style = "ui green message"
            messages.success(request, 'Refresher Form has been Recorded!')
            return redirect('deployment:daily_refresher_form')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'form':form,
        'dr':dr,
        'style':style,
    }


    return render(request, 'deployment/daily_refresher_form.html', context)

#TODO: this
def incident_detail(request, id):
    incident = Incidents.objects.get(id = id)
    title = "Incident Detail View"


    # NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context ={
        'incident' : incident,
        'title': title,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'deployment/incident_detail.html', context)

def deployment_report(request):

    from_date = request.session["session_fromdate"]
    to_date = request.session["session_todate"]
    requestdog = Dog_Request.objects.filter(start_date__range = [from_date, to_date])
    incident = Incidents.objects.filter(date__range = [from_date, to_date])
    user = request.session["session_username"]
    team = Team_Assignment.objects.filter(date_added__range = [from_date, to_date])
    deployed = Team_Dog_Deployed.objects.filter(date_added__range = [from_date, to_date]).filter(date_pulled__range = [from_date, to_date])

    context = {
        'title': "",
        'requestdog': requestdog,
        'from_date': from_date,
        'to_date': to_date,
        'incident': incident,
        'user': user,
        'team': team,
        'deployed': deployed,
    }
    return render(request, 'deployment/deployment_report.html', context)


def choose_location(request):

    #TODO Add user field to TempDeployment to avoid issues when multiple users are using the system at the same time (also check ancestral view from training module)
    removal = TempDeployment.objects.all()
    removal.delete()

    locations = Location.objects.all()

    location_incident_count_list = []
    location_maritime_count_list = []
    location_list = []
    team_list = []
    for location in locations:
        incident_count = Incidents.objects.filter(location=location).count()
        location_incident_count_list.append(incident_count)
        maritime_count = Maritime.objects.filter(location=location).count()
        location_maritime_count_list.append(maritime_count)
        team = Team_Assignment.objects.get(location = location)
        location_list.append(location)
        team_list.append(team)

    df_data = {
        'Location': location_list,
        'Maritime': location_maritime_count_list,
        'Incident': location_incident_count_list,
        'Team' : team_list
    }
    location_dataframe = df(data=df_data)
    location_dataframe.sort_values(by=['Maritime', 'Incident'], ascending=[True, True])

    context = {
        'locations': location_dataframe,
    }

    return render(request, 'deployment/location_list.html', context)

#TODO filter units available by capability if the number has already met demand requirements
#TODO add counter for units that are set for deployment
#TODO sort units by incident count

#TODO capability_blacklist only updates when another location is selected
def load_units(request):

    selected_list = []

    location_id = request.GET.get('location')
    location = Location.objects.get(id = location_id)

    # filter personal_info where city != Team_Assignment.city
    handlers = Personal_Info.objects.exclude(city=location.city)

    user_deploy = []
    for h in handlers:
        user_deploy.append(h.UserID)

    capability_blacklist = []

    team = Team_Assignment.objects.get(location=location)

    sar_count_select = 0
    ndd_count_select = 0
    edd_count_select = 0

    try: #The solution lies on the checkbox initial values right here
        fullstring = request.GET.get('fullstring')
        fullstring = json.loads(fullstring)

        print("FullString")
        print(fullstring)

        for item in fullstring.values(): # item == checked checkboxes
            selected_list.append(item)

        print("SELECTED LIST")
        print(selected_list)

        # START TEST


        temp = TempDeployment.objects.filter(location=location)
        k9s = K9.objects.filter(pk__in = selected_list)

        print("TEMP OBJECTS")
        print(temp)

        for item in temp:
            if item.k9.capability == "SAR":
                sar_count_select += 1
            elif item.k9.capability == "NDD":
                ndd_count_select += 1
            else:
                edd_count_select += 1

        if (team.EDD_deployed + edd_count_select) >= team.EDD_demand:
            capability_blacklist.append("EDD")
        if (team.NDD_deployed + ndd_count_select) >= team.NDD_demand:
            capability_blacklist.append("NDD")
        if (team.SAR_deployed + sar_count_select) >= team.SAR_demand:
            capability_blacklist.append("SAR")

        print("CAPABILITY BLACKLIST")
        print(capability_blacklist)

        print(sar_count_select)
        print(ndd_count_select)
        print(edd_count_select)

        # END TEST

    except:
        pass

    # #filter K9 where handler = person_info and k9 assignment = None
    can_deploy = K9.objects.filter(handler__in=user_deploy).filter(training_status='For-Deployment').filter(
        assignment='None').exclude(capability__in=capability_blacklist)

    context = {
        'location': location,
        'can_deploy' : can_deploy,
        'selected_list' : selected_list,
        'team' : team,
        'sar': sar_count_select,
        'ndd': ndd_count_select,
        'edd': edd_count_select
    }

    return render(request, 'deployment/ajax_load_units.html', context)


def load_units_selected(request): #Note : Maybe we can use a db solution for this one

    scheduleFormset = formset_factory(ScheduleUnitsForm, extra=1, can_delete=True)

    fullstring = request.GET.get('fullstring')
    fullstring = json.loads(fullstring)

    k9_list = []
    k9_list_id = []

    try:
        location_id = request.GET.get('location')
        location = Location.objects.get(id=location_id)

        for item in fullstring.values():
            k9 = K9.objects.get(id=item)
            k9_list.append(k9)
            k9_list_id.append(k9.id)

            # >>>>>>>

            if TempDeployment.objects.filter(k9=k9).exists():
                pass
            else:
                temp = TempDeployment.objects.create(location=location, k9=k9)
                temp.save()

                removal = TempDeployment.objects.exclude(id=temp.id).filter(k9=k9).filter(
                    location=location)  # hindi dapat idelete yung previously saved
                removal.delete()

    except:
        for item in fullstring.values():
            k9 = K9.objects.get(id=item)
            k9_list.append(k9)
            k9_list_id.append(k9.id)

            # >>>>>>>

            if TempDeployment.objects.filter(k9=k9).exists():
                pass
            else:
                removal = TempDeployment.objects.filter(k9=k9)  # Dapat icheck niya kung ano yung mga hindi naka select
                removal.delete()


    can_deploy = K9.objects.filter(training_status='For-Deployment').filter(
        assignment='None').exclude(pk__in= k9_list_id)

    removal = TempDeployment.objects.exclude(k9__in=k9_list)
    removal.delete()

    temp_deploy = TempDeployment.objects.all()

    k9_list_id = list(dict.fromkeys(k9_list_id))

    context = {
        'can_deploy': can_deploy,
        'temp_deploy' : temp_deploy,
        'formset' : scheduleFormset,
        'selected_list' : k9_list_id
    }

    return render(request, 'deployment/ajax_load_units_selected.html', context)

#TODO Include K9 Backups
def schedule_units(request):

    removal = TempDeployment.objects.all() #TODO add user field then only delete objects from said user
    removal.delete()

    # Prioritize Locations
    locations = Location.objects.all()
    location_incident_list = []
    location_maritime_list = []
    location_list = []
    team_list = []
    total_dogs_deployed_list = []
    incident_order_list = []

    location_incident_list_count = []
    location_maritime_list_count = []
    for location in locations:
        maritimes = Maritime.objects.filter(location=location)
        location_maritime_list.append(maritimes)
        incidents = Incidents.objects.filter(location=location)
        location_incident_list.append(incidents)

        location_incident_list_count.append(maritimes.count())
        location_maritime_list_count.append(incidents.count())

        team = Team_Assignment.objects.get(location=location)
        location_list.append(location)
        team_list.append(team)

        #dogs_scheduled_count = Team_Dog_Deployed.objects.filter(status = "Scheduled", team_assignment = team).count()
        dogs_scheduled_count = K9_Schedule.objects.filter(status = "Initial Deployment", team = team).count()

        total_dogs_deployed_list.append(team.total_dogs_deployed + dogs_scheduled_count) #TODO Include scheduled K9s

        #Sort incidents
        incident_type_list = []
        incident_type_order_list = []
        for incident in incidents:
            type = incident.type
            incident_type_list.append(type)


        #order incident_type_order_list[] by the most count from incident_type_list[]
        sar_incident = 0
        ndd_incident = 0
        edd_incident = 0
        for type in incident_type_list:
            if type == "Search and Rescue Related":
                sar_incident += 1
            elif type == "Narcotics Related":
                ndd_incident += 1
            elif type == "Explosives Related":
                edd_incident += 1
            else:
                pass


        incident_type_order_list.append(('SAR', sar_incident))
        incident_type_order_list.append(('NDD', ndd_incident))
        incident_type_order_list.append(('EDD', edd_incident))

        #incident_type_order_list.sort(reverse=True)#TODO find a way to sort a list of tuples
        incident_type_order_list.sort(key=lambda  tup: tup[1], reverse=True)

        incident_order_list.append(incident_type_order_list)

        #Replace code up to this point with a better version (too loopy and hardcody)

    #TODO add incident_type_order_list[] to the dataframe columns
    #TODO Add currently scheduled to templates
    df_data = {
        'Location': location_list,
        'Maritime': location_maritime_list,
        'Incident': location_incident_list,
        'Maritime_count': location_maritime_list_count,
        'Incident_count': location_incident_list_count,
        'Incident_Order_List': incident_order_list,
        'Team': team_list,
        'Dogs_deployed': total_dogs_deployed_list
        }
    location_dataframe = df(data=df_data)
    location_dataframe.sort_values(by=['Dogs_deployed', 'Maritime_count', 'Incident_count'], ascending=[True, False, False])


         #End Sort incidents

    # End Prioritize Location

    #Temporary assignment
    end_assignment = 0
    iteration = 0

    k9s_scheduled_list = []
    #k9s_scheduled = Team_Dog_Deployed.objects.filter(status="Scheduled")
    k9s_scheduled = K9_Schedule.objects.filter(status="Initial Deployment")

    for item in k9s_scheduled:
        k9s_scheduled_list.append(item.k9.id)

    # can_deploy = K9.objects.filter(training_status='For-Deployment').filter(
    #     assignment='None').exclude(pk__in=k9s_scheduled_list)


    while end_assignment == 0:

        #Solution 2: Loop through dataframe first
        for item in location_dataframe.values:
            incident_type_selected = 0
            location = item[0]
            incident_type_list = item[5]
            team = item[6]  #check if only 1 unit is assigned (must be 2)

            temp = TempDeployment.objects.all()  # add user field to avoid complications involving multiple users in the future
            k9_id_list = []
            for item in temp:
                k9_id_list.append(item.k9.id)

            # Get K9s ready for deployment #TODO Include schedule K9s
            can_deploy = K9.objects.filter(training_status='For-Deployment').filter(
                assignment='None').exclude(pk__in=k9_id_list).exclude(pk__in=k9s_scheduled_list)
            # End Get K9s ready for deployment

            k9s_assigned = 0
            finish_location_assignment = 0
            for k9 in can_deploy:
                if finish_location_assignment == 0:
                    type = incident_type_list[iteration][0] #TODO Dapat hanapin muna yung priority skill from list of k9s. If wala, go to next priority sa next iteration
                    if type == k9.capability:

                        sar_count = 0
                        ndd_count = 0
                        edd_count = 0
                        for item in TempDeployment.objects.filter(location = location):
                            if item.k9.capability == "SAR":
                                sar_count += 1
                            elif item.k9.capability == "NDD":
                                ndd_count += 1
                            elif item.k9.capability == "EDD":
                                edd_count += 1
                            else: pass

                        if type == "SAR":
                            if team.SAR_deployed + sar_count < team.SAR_demand:
                                TempDeployment.objects.create(k9=k9, location=location)
                                k9s_assigned += 1

                        elif type == "NDD":
                            if team.NDD_deployed + ndd_count < team.NDD_demand:
                                TempDeployment.objects.create(k9=k9, location=location)
                                k9s_assigned += 1

                        elif type == "EDD":
                            if team.EDD_deployed + edd_count < team.EDD_demand:
                                TempDeployment.objects.create(k9=k9, location=location)
                                k9s_assigned += 1

                        else:
                            pass

                    # dogs_scheduled_count = Team_Dog_Deployed.objects.filter(status="Scheduled",
                    #                                                         team_assignment = team).count()
                    dogs_scheduled_count = K9_Schedule.objects.filter(status = "Initial Deployment", team = team).count()
                    if (team.total_dogs_deployed + k9s_assigned + dogs_scheduled_count) >= 2: #There must be atleast 2 units per location #TODO Include schedule K9s
                        print("Units per Location " + str(location))
                        print(team.total_dogs_deployed + k9s_assigned)
                        finish_location_assignment = 1




        if iteration == 2:
            end_assignment = 1
        else:
            iteration += 1


    temp = TempDeployment.objects.all()  # add user field to avoid complications involving multiple users in the future
    locations = Location.objects.all()
    k9_id_list = []

    locations = list(location_dataframe['Location'])

    for location in locations:
        temp_count = 0
        for item in temp:
            if item.location == location:
                temp_count += 1

        if temp_count < 2:
            removal = TempDeployment.objects.filter(location=location) #TODO add user field then only delete objects from said user
            removal.delete()


    temp = TempDeployment.objects.all()
    for item in temp:
        k9_id_list.append(item.k9.id)

    temp_list = []
    for location in locations:
        temp = TempDeployment.objects.filter(location = location)
        temp_list.append(temp)


    # Get K9s ready for deployment
    can_deploy = K9.objects.filter(training_status='For-Deployment').filter(
        assignment='None').exclude(pk__in=k9_id_list).exclude(pk__in=k9s_scheduled_list)

    #End Temporary assignment

    # TODO Add TempAssignments to dataframe, don't reinitialize

    location_dataframe['Temp_list'] = temp_list

    # data = location_dataframe.set_index("Temp_list")
    # data = data.drop(None, axis=0)


    temp_list = list(location_dataframe['Temp_list'])

    idx = 0
    delete_indexes = []
    for item in temp_list:
        if not item:
            delete_indexes.append(idx)
        idx += 1

    print("DELETE INDEXES")
    print(delete_indexes)

    location_dataframe.drop(location_dataframe.index[delete_indexes], inplace=True) #Delete rows without any K9s assigned
    location_dataframe.reset_index(drop=True, inplace=True)

    team_list = list(location_dataframe['Team'])
    locations = list(location_dataframe['Location'])
    temp_list = list(location_dataframe['Temp_list'])

    schedFormset = formset_factory(DeploymentDateForm, extra=len(locations))
    formset = schedFormset(request.POST or None)

    style = ""

    print(location_dataframe)

    if request.method == 'POST':
        if  formset.is_valid:

            idx = 0
            for form in  formset:
                if form.is_valid:
                    try:
                        deployment_date = form['deployment_date'].value()
                        deployment_date = datetime.datetime.strptime(deployment_date, "%Y-%m-%d").date()
                        print("Deployment Date")
                        print(deployment_date)

                        delta = deployment_date - datetime.date.today()
                        print("Delta")
                        print(delta.days)
                        if delta.days < 7:
                            style = "ui red message"
                            messages.warning(request, 'Dates should have atleast 1 week allowance')
                        else:
                            team = team_list[idx]
                            temp = temp_list[idx]

                            print("Temp")
                            print(temp)
                            for item in temp:
                                print("Item")
                                print(item)
                                #deploy = Team_Dog_Deployed.objects.create(team_assignment = team, k9 = item.k9, status = "Scheduled", date_added = deployment_date)
                                deploy = K9_Schedule.objects.create(team = team, k9 = item.k9, status = "Initial Deployment", date_start = deployment_date)
                                deploy.save()
                                pre_req_item = K9_Pre_Deployment_Items.objects.create(k9 = item.k9, initial_sched = deploy)
                                pre_req_item.save()
                            style = "ui green message"
                            messages.success(request, 'Units have been successfully scheduled for deployment!')
                    except:
                        pass

    df_is_empty = False
    if location_dataframe.empty:
        df_is_empty = True

    context = {
        'df' : location_dataframe,
        'can_deploy': can_deploy,
        'temp': TempDeployment.objects.all(),
        'formset' :schedFormset,
        'style': style,
        'df_is_empty' : df_is_empty,
    }

    return render(request, 'deployment/schedule_units.html', context)


