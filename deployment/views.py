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


import datetime
import re
import sys
from datetime import date

from unitmanagement.models import Notification
from training.models import K9_Handler
from planningandacquiring.models import K9
from profiles.models import Personal_Info, User, Account
from inventory.models import Medicine

from deployment.models import Area, Location, Team_Assignment, Team_Dog_Deployed, Dog_Request, K9_Schedule, Incidents

from deployment.forms import AreaForm, LocationForm, AssignTeamForm, EditTeamForm, RequestForm, IncidentForm, GeoForm, MonthYearForm, GeoSearch, DateForm
from deployment.models import Area, Location, Team_Assignment, Team_Dog_Deployed, Dog_Request, K9_Schedule, Incidents, Daily_Refresher, K9_Pre_Deployment_Items

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
from datetime import datetime, timedelta, date

from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe

from deployment.util import Calendar, get_date, prev_month, next_month, select_month, Calendar_Detailed


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
    d = K9_Pre_Deployment_Items.objects.filter(status='Complete')



    context = {
      'title':'Deployment',
      'd':d,
    }
    return render (request, 'deployment/index.html', context)

def add_area(request):
    form = AreaForm(request.POST or None)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Area has been successfully Added!')
            form = AreaForm()
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
        if form.is_valid():
            location = form.save()

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
            
            #Location
            l=Location.objects.get(id=f.location.id)
            l.status = 'assigned'

            #Team Leader
            u = User.objects.get(id=f.team_leader.id)
            u.assigned = True

            l.save()
            u.save()

            style = "ui green message"
            return redirect('deployment:assigned_location_list')
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
    user = user_session(request)
    data = Team_Assignment.objects.all()

    if user.position == 'Commander':
        data = Team_Assignment.objects.filter(location__area.commanderuser)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
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
    print(data.id)
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

    geoform = GeoForm(request.POST or None)
    geosearch = GeoSearch(request.POST or None)
    width = 470

    style = ""

    if request.method == 'POST':
        print(form.errors)
        form.validate_date()
        if form.is_valid():

            cd = form.cleaned_data['phone_number']
            regex = re.compile('[^0-9]')
            form.phone_number = regex.sub('', cd)

            location = form.save()

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
    return render (request, 'deployment/request_form.html', context)
    

def request_dog_list(request):
    data = Dog_Request.objects.all()

    date_now = datetime.date.today()
    latest_date = Dog_Request.objects.latest('end_date')
    latest_date = latest_date.end_date

    k9_schedule = Dog_Request.objects.filter(end_date__range=[str(date_now), str(latest_date)])
    gantt_chart_dict = []

    # TODO Remove finished requests and add current date marker
    for sched in k9_schedule:
        data_list = {"Task": str(sched),
                     "Start": str(sched.start_date),
                     "Finish": str(sched.end_date),
                     "Resource": str(sched.status)}
        gantt_chart_dict.append(data_list)

    colors = dict(Pending='rgb(255, 0, 0)',
                  Approved='rgb(0, 0, 255)',)

    # df = [   dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
    #       dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
    #       dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30') ]

    if gantt_chart_dict:
        df = gantt_chart_dict

        title = "Schedule of Upcoming Requests"
        fig = ff.create_gantt(df, colors=colors, title=title, group_tasks=True, showgrid_x=True, showgrid_y=True,
                          bar_width=0.6, index_col='Resource', show_colorbar=True)
        gantt_chart = opy.plot(fig, auto_open=False, output_type='div')
    else:
        gantt_chart = "There are no upcoming requests scheduled!"

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'data': data,
        'title': 'Request Dog List',
        'gantt_chart': gantt_chart,
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
    handlers = Personal_Info.objects.exclude(city=data2.area.city)

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


    #>>>> start of new Code for saving schedules instead of direct deployment
    # TODO Filter can deploy to with teams without date conflicts
    can_deploy_filtered = []
    for k9 in can_deploy:
        #1 = true, 0 = false
        deployable = 1
        schedules = K9_Schedule.objects.filter(k9=k9)
        print("can_deploy")
        print(k9)
        #TODO obtain schedule of request then compare to start and end date of schedules (loop)
        for sched in schedules:
            if (sched.date_start >= data2.start_date and sched.date_start <= data2.end_date) or (sched.date_end >= data2.start_date and sched.date_end <= data2.end_date) or (data2.start_date >= sched.date_start and data2.start_date <= sched.date_end) or (data2.end_date >= sched.date_start and data2.end_date <= sched.date_end):
                deployable = 0

        if deployable == 1:
            can_deploy_filtered.append(k9.id)

    can_deploy2 =  K9.objects.filter(id__in = can_deploy_filtered) #Trained and Assigned dogs without date conflicts TODO Can be displayed but disabled and tagged
    #TODO If a dog is deployed to a request, the dog will only be deployed if system datetime is same as scheduled request.
    #>>Also, dog deployment means scheduling first

    #>>Use can_deploy2 instead of can_deploy or assign can_deplyo2 to can_deploy
    can_deploy = can_deploy2

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
            Team_Dog_Deployed.objects.create(team_requested=data2, k9=checked_dogs, status="Scheduled", handler = str(k9.handler.fullname)) #TODO Only save k9.assignment when system datetime is same as request
            
            K9_Schedule.objects.create(k9 = checked_dogs, dog_request = data2, date_start = data2.start_date, date_end = data2.end_date)

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
    latest_date = K9_Schedule.objects.latest('date_end')
    latest_date = latest_date.date_end

    k9 = K9.objects.get(id = id)
    k9_schedule = K9_Schedule.objects.filter(k9=k9).filter(date_end__range=[str(date_now), str(latest_date)])

    gantt_chart_dict = []

    #TODO Remove finished requests and add current date marker
    for sched in k9_schedule:
        data_list = {"Task": str(sched.dog_request),
                     "Start": str(sched.date_start),
                     "Finish": str(sched.date_end)}
                     #"Resource": str()}
        gantt_chart_dict.append(data_list)


    # df = [   dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
    #       dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
    #       dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30') ]

    if gantt_chart_dict:
        df = gantt_chart_dict

        title = "Upcoming Requests Schedule for " + str(k9)
        fig = ff.create_gantt(df, title=title, group_tasks=True, showgrid_x=True, showgrid_y=True,
                           bar_width=0.6)
        gantt_chart = opy.plot(fig, auto_open=False, output_type='div')
    else:
        gantt_chart = "There are no upcoming schedules for "+str(k9)+ ", go to the Request List to assign K9 to a request."

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'k9' : k9,
        'gantt_chart': gantt_chart,
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

    ta = Team_Assignment.objects.get(team_leader=current_user)


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


