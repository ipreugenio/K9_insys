from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
import datetime

from training.models import K9_Handler
from planningandacquiring.models import K9
from profiles.models import Personal_Info, User
from inventory.models import Medicine
from deployment.models import Area, Location, Team_Assignment, Team_Dog_Deployed, Dog_Request, K9_Schedule, Incidents
from deployment.forms import AreaForm, LocationForm, AssignTeamForm, EditTeamForm, RequestForm, IncidentForm

#Plotly
import plotly.offline as opy
import plotly.graph_objs as go
import plotly.graph_objs.layout as lout
import plotly.figure_factory as ff

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
    context = {
      'title':'Add Area Form',
      'texthelp': 'Input Name of Area Here',
      'form': form,
      'actiontype': 'Submit',
      'style':style,
    }
    return render (request, 'deployment/add_area.html', context)

def add_location(request):
    form = LocationForm(request.POST or None)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Location has been successfully Added!')
            form = LocationForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    context = {
      'title':'Add Location Form',
      'texthelp': 'Input Location Details Here',
      'form': form,
      'actiontype': 'Submit',
      'style':style,
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
    context = {
      'title':'Assign Team to Location',
      'texthelp': 'Input Team and Location Details Here',
      'form': form,
      'actiontype': 'Submit',
      'style':style,
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
    context = {
      'title': data.team,
      'texthelp': 'Edit Team Details Here',
      'form': form,
      'data': data,
      'actiontype': 'Submit',
      'style':style,
    }
    return render(request, 'deployment/edit_team.html', context)

def assigned_location_list(request):
    data = Team_Assignment.objects.all()
    context = {
        'title' : 'DOGS AND HANDLERS ASSIGNED FOUs',
        'data' : data
    }

    return render(request, 'deployment/assigned_location_list.html', context)

def team_location_details(request, id):
    data = Team_Assignment.objects.get(id=id)
    k9 = Team_Dog_Deployed.objects.filter(team_assignment=data)
    incidents = Incidents.objects.filter(location = data.location)
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

    context = {
        'title' : data,
        'data' : data,
        'k9' : k9,
        'can_deploy':can_deploy,
        'style': style,
        'dogs_deployed':dogs_deployed,
        'dogs_pulled': dogs_pulled,
        'sar_inc': sar_inc,
        'ndd_inc': ndd_inc,
        'edd_inc': edd_inc
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
    style = ""
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Request has been successfully Added!')
            form = RequestForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    context = {
      'title':'Request Form',
      'texthelp': 'Input request of client here.',
      'form': form,
      'actiontype': 'Submit',
      'style':style,
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

    context = {
        'data': data,
        'title': 'Request Dog List',
        'gantt_chart': gantt_chart
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
    # dogs deployed
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
        #TODO obtain schedule of request then compare to start and end date of schedules (loop)
        for sched in schedules:
            if (sched.date_start >= data2.start_date and sched.date_start <= data2.end_date) or (sched.date_end >= data2.start_date and sched.date_end <= data2.end_date):
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
            Team_Dog_Deployed.objects.create(team_requested=data2, k9=checked_dogs, status="Scheduled") #TODO Only save k9.assignment when system datetime is same as request

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

    context = {
        'title': data2,
        'data2': data2,
        'can_deploy': can_deploy,
        'style': style,
        'dogs_deployed': dogs_deployed,
    }

    return render(request, 'deployment/request_dog_details.html', context)

def remove_dog_request(request, id):
    pull_k9 = Team_Dog_Deployed.objects.get(id=id)
    k9 = K9.objects.get(id=pull_k9.k9.id)
    dog_request = Dog_Request.objects.get(id=pull_k9.team_requested.id)

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

def deployment_report(request):
    assignment = Team_Assignment.objects.all()


    context = {
        'title': 'Request Dog List',
        'assignment': assignment,

    }
    return render (request, 'deployment/request_dog_list.html', context)


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


    context = {
        'k9' : k9,
        'gantt_chart': gantt_chart
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
    context = {
        'title': 'Report Incident Form',
        'texthelp': 'Input Incident Details Here',
        'form': form,
        'actiontype': 'Submit',
        'style': style,
    }
    return render(request, 'deployment/incident_form.html', context)

def incident_list(request):
    title = "Incidents List View"
    incidents = Incidents.objects.all()

    context = {
        'incidents': incidents,
        'title': title
    }

    return render(request, 'deployment/incident_list.html', context)