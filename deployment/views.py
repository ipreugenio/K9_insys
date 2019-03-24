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

from deployment.forms import AreaForm, LocationForm, AssignTeamForm, EditTeamForm, RequestForm, IncidentForm, DateForm

from deployment.forms import AreaForm, LocationForm, AssignTeamForm, EditTeamForm, RequestForm, IncidentForm, GeoForm, MonthYearForm


#Plotly
'''import plotly.offline as opy
import plotly.graph_objs as go
import plotly.graph_objs.layout as lout
import plotly.figure_factory as ff'''


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

    context = {
      'title':'Deployment'
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
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            new_form = form.save()
            location = Location.objects.get(id = new_form.pk)
            style = "ui green message"
            messages.success(request, 'Location has been successfully Added!')

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
      'actiontype': 'Submit',
      'style':style,
      'notif_data':notif_data,
      'count':count,
      'user':user,
    }
    return render (request, 'deployment/add_location.html', context)

def assign_team_location(request):
    form = AssignTeamForm(request.POST or None)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            location = form.cleaned_data['location']
            l = Location.objects.get(id=location.id)

            #change the status of the location
            data = Location.objects.get(id=l.id)
            data.status = 'assigned'
            data.save()

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
    request.session['team_assignment_id'] = id
    if 'dog_request_id' in request.session:
        del request.session['dog_request_id']

    #TODO retrieve K9 objects taht are currently deployed in ports but not in requests. Then use them as "location transferrals"

    data = Team_Assignment.objects.get(id=id)
    k9 = Team_Dog_Deployed.objects.filter(team_assignment=data)
    incidents = Incidents.objects.filter(location = data.location).count()
    edd_inc = Incidents.objects.filter(location = data.location).filter(type = "Explosives Related").count()
    ndd_inc = Incidents.objects.filter(location=data.location).filter(type="Narcotics Related").count()
    sar_inc = Incidents.objects.filter(location=data.location).filter(type="Search and Rescue Related").count()
    style = ""
    #filter personal_info where city != Team_Assignment.city
    handlers = Personal_Info.objects.exclude(city=data.location.city)

    handler_can_deploy=[] # append the id of the handlers
    for h in handlers:
        handler_can_deploy.append(h.id)
    #print(handler_can_deploy)

    #get instance of user using personal_info.id
    #id of user is the fk.id of person_info
    user = User.objects.filter(id__in=handler_can_deploy)
    #print(user)

    user_deploy=[] # append the user itself
    for u in user:
        user_deploy.append(u.id)

    # print(user_deploy)
    # #filter K9 where handler = person_info and k9 assignment = None
    can_deploy = K9.objects.filter(handler__id__in=user_deploy).filter(training_status='For-Deployment').filter(assignment='None')
    #print(can_deploy)

    #dogs deployed
    dogs_deployed = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(status='Deployed')
    dogs_pulled = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(status='Pulled-Out')
    team_dog_deployed = Team_Dog_Deployed.objects.filter(team_assignment=data)

    #Dogs the can be transferred from one port to another
    location_k9s = [] # Deployed K9s assigned to ports
    team_assignments = Team_Assignment.objects.exclude(id = data.id) #Exclude current assignment from available port transferals
    deployed_k9s = K9.objects.filter(handler__id__in=user_deploy).filter(training_status="Deployed").exclude(assignment='None').exclude(assignment = data)# Retrieve K9s deployed
    can_transfer = None

    print("Deployed K9s")
    print(deployed_k9s)

    if deployed_k9s:
        for k9 in deployed_k9s: #Retrieve K9s deployed in ports
            assignment_check = 0
            for team_assignment in team_assignments:
                if str(k9.assignment) == str(team_assignment):
                    print(k9.assignment)
                    print(team_assignment)
                    assignment_check = 1
            if assignment_check == 1:
                location_k9s.append(k9.id)
        can_transfer = K9.objects.filter(pk__in = location_k9s) #TODO Add these to Location Deployment

    print("CAN_TRANSFER")
    print(can_transfer)

    if request.method == 'POST':
        checks =  request.POST.getlist('checks') # get the id of all the dogs checked
        #print(checks)

        #get the k9 instance of checked dogs
        checked_dogs = K9.objects.filter(id__in=checks)
        #print(checked_dogs)
        print("CHECKED DOGS")
        print(checked_dogs)
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
            dog.training_status = "Deployed"
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
        'can_deploy':can_deploy,
        'style': style,
        'dogs_deployed':dogs_deployed,
        'dogs_pulled': dogs_pulled,
        'sar_inc': sar_inc,
        'ndd_inc': ndd_inc,
        'edd_inc': edd_inc,

        'incidents': incidents,
        'can_transfer' : can_transfer,
        'team_dog_deployed': team_dog_deployed,

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
    pull_k9.date_pulled = date.today()
    pull_k9.save()

    #change K9 model
    k9.assignment = 'None'
    k9.training_status = "For-Deployment"
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
    style = ""

    if request.method == 'POST':
        if form.is_valid() and geoform.is_valid():
            form.validate_date()
            cd = form.cleaned_data['phone_number']
            regex = re.compile('[^0-9]')
            form.phone_number = regex.sub('', cd)

            new_form = form.save()
            dog_request = new_form.pk
            dog_request = Dog_Request.objects.get(id = dog_request)

            style = "ui green message"
            messages.success(request, 'Request has been successfully Added!')
            #form = RequestForm()

            #checks = request.POST['point']
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

            #request_coordinates = Request_Coordinates.objects.create(dog_request = dog_request, longtitude = lon, latitude = lat)
            dog_request.longtitude = lon
            dog_request.latitude = lat
            dog_request.save()

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
      'actiontype': 'Submit',
      'style':style,
      'notif_data':notif_data,
      'count':count,
      'user':user,
    }
    return render (request, 'deployment/request_form.html', context)

def request_dog_list(request):
    data = Dog_Request.objects.all()
    monthyearform = MonthYearForm(request.POST or None)
    month = None
    # use today's date for the calendar if None, else get input
    if request.method == 'POST':
        for each in monthyearform:
            print("POST DATE")
            print(each.value())
            month = select_month(each.value())

        d = get_date(month)
    else:
        d = get_date(request.GET.get('month', None))

    print("DATE TEST")
    print(d)

    # Instantiate our calendar class with today's year and date
    cal = Calendar(d.year, d.month)

    # Call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(withyear=True)
    #context['calendar'] = mark_safe(html_cal)

    previous = prev_month(d)
    next = next_month(d)

    print("PREVIOUS")
    print(previous)
    print("NEXT")
    print(next)

    print("REQUEST")
    print(request)

    date_today = date.today()

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'data': data,
        'title': 'Request Dog List',

        # 'gantt_chart': gantt_chart,
        'calendar': mark_safe(html_cal),
        'prev_month': previous,
        'next_month': next,
        'monthyearform': monthyearform,
        'date_today': date_today,

        'notif_data':notif_data,
        'count':count,
        'user':user,

    }
    return render (request, 'deployment/request_dog_list.html', context)

def request_dog_details(request, id):
    request.session['dog_request_id'] = id
    if 'team_assignment_id' in request.session:
        del request.session['team_assignment_id']

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
    # #filter K9 where handler = person_info
    can_deploy = K9.objects.filter(handler__id__in=user_deploy).filter(Q(training_status='For-Deployment') | Q(training_status='Deployed'))#.filter(assignment='None')
    # print(can_deploy)

    # dogs deployed to Dog Request
    dogs_deployed = Team_Dog_Deployed.objects.filter(team_requested=data2) #.filter(status='Deployed')

    #>>>> start of new Code for saving schedules instead of direct deployment
    # TODO Filter can deploy to with teams without date conflicts
    can_deploy_filtered = []
    for k9 in can_deploy:
        #1 = true, 0 = false
        deployable = 1
        schedules = K9_Schedule.objects.filter(k9=k9)
        print("can_deploy")
        print(k9)

        for sched in schedules:
            if (sched.date_start >= data2.start_date and sched.date_start <= data2.end_date) or (sched.date_end >= data2.start_date and sched.date_end <= data2.end_date):
                deployable = 0

        if deployable == 1:
            can_deploy_filtered.append(k9.id)

    can_deploy2 =  K9.objects.filter(id__in = can_deploy_filtered) #Trained and Assigned dogs without date conflicts
    #TODO If a dog is deployed to a request, the dog will only be deployed if system datetime is same as scheduled request.
    #>>Also, dog deployment means scheduling first

    #>>Use can_deploy2 instead of can_deploy or assign can_deplyo2 to can_deploy
    can_deploy = can_deploy2

    if request.method == 'POST':
        if 'approve' in request.POST:
            data2.remarks = request.POST.get('remarks')
            data2.status = "Approved"
            data2.save()
            return HttpResponseRedirect('../request_dog_list/')
        elif 'deny' in request.POST:
            data2.remarks = request.POST.get('remarks')
            data2.status = "Denied"
            data2.save()
            return HttpResponseRedirect('../request_dog_list/')

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

    #change Team_Dog_Deployed model
    pull_k9.status = 'Pulled-Out'
    pull_k9.date_pulled = date.today()
    pull_k9.save()

    #change K9 model
    #k9.assignment = 'None'
    #k9.save()
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

def deployment_report(request):
    assignment = Team_Assignment.objects.all()

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': 'Request Dog List',
        'assignment': assignment,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'deployment/request_dog_list.html', context)


def view_schedule(request, id):
    team_assignment_id = None
    dog_request_id = None
    if 'team_assignment_id' in request.session:
        team_assignment_id = request.session['team_assignment_id']
        del request.session['team_assignment_id']

    if 'dog_request_id' in request.session:
        dog_request_id = request.session['dog_request_id']
        del request.session['dog_request_id']


    k9 = K9.objects.get(id = id)
    schedules = K9_Schedule.objects.filter(k9 = k9)

    monthyearform = MonthYearForm(request.POST or None)
    month = None
    # use today's date for the calendar if None, else get input
    if request.method == 'POST':
        for each in monthyearform:
            print("POST DATE")
            print(each.value())
            month = select_month(each.value())

        d = get_date(month)
    else:
        d = get_date(request.GET.get('month', None))

    print("DATE TEST")
    print(d)

    # Instantiate our calendar class with today's year and date
    cal = Calendar_Detailed(d.year, d.month, id)

    # Call the formatmonth method, which returns our calendar as a table
    html_cal = cal.formatmonth(withyear=True)
    # context['calendar'] = mark_safe(html_cal)

    previous = prev_month(d)
    next = next_month(d)


    date_today = date.today()

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {
        'k9' : k9,
        'calendar': mark_safe(html_cal),
        'prev_month': previous,
        'next_month': next,
        'monthyearform': monthyearform,
        'team_assignment_id': team_assignment_id,
        'dog_request_id': dog_request_id,
        'date_today': date_today,
        'schedules': schedules,

        'notif_data':notif_data,
        'count':count,
        'user':user,

    }

    return render(request, 'deployment/k9_schedule.html', context)

'''
def load_teams(request):
    area_id = request.GET.get('area')
    area = Area.objects.get(id = area_id)
    teams = Team.objects.filter(area=area).order_by('name')

    return render(request, 'deployment/ajax_load_teams.html', {'teams': teams})
'''

def add_incident(request):
    form = IncidentForm(request.POST or None)
    style = ""

    user_serial = request.session['session_serial']
    user = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user.UserID.id)

    if request.method == 'POST':
        if form.is_valid():
            incident = form.save()
            incident.user = current_user
            incident.save()
            
            style = "ui green message"
            messages.success(request, 'Incident has been successfully added!')
            form = IncidentForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
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

    if request.method == 'POST':
        if form.is_valid():
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            request.session["session_fromdate"] = from_date
            request.session["session_todate"] = to_date

            return HttpResponseRedirect('deployment-report/')

    context = {
        'title': "",
        'form': form,
    }
    return render(request, 'deployment/choose_date.html', context)

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

