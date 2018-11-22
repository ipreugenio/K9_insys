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
from deployment.models import Area, Location, Team_Assignment, Team_Dog_Deployed, Dog_Request
from deployment.forms import AreaForm, LocationForm, AssignTeamForm, EditTeamForm, RequestForm
# Create your views here.

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
            Team_Dog_Deployed.objects.create(team_assignment=data, k9=checked_dogs)
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

    context = {
        'data': data,
        'title': 'Request Dog List',
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

    # print(user_deploy)
    # #filter K9 where handler = person_info and k9 assignment = None
    can_deploy = K9.objects.filter(handler__id__in=user_deploy).filter(training_status='For-Deployment').filter(
        assignment='None')
    # print(can_deploy)

    # dogs deployed
    dogs_deployed = Team_Dog_Deployed.objects.filter(team_requested=data2).filter(status='Deployed')

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
            Team_Dog_Deployed.objects.create(team_requested=data2, k9=checked_dogs)
            # TODO: if dog is equal capability increment
            if checked_dogs.capability == 'EDD':
                data2.EDD_deployed = data2.EDD_deployed + 1
            elif checked_dogs.capability == 'NDD':
                data2.NDD_deployed = data2.NDD_deployed + 1
            else:
                data2.SAR_deployed = data2.SAR_deployed + 1

            data2.save()
            dog = K9.objects.get(id=checked_dogs.id)
            dog.assignment = str(data2)
            dog.save()

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


'''
def load_teams(request):
    area_id = request.GET.get('area')
    area = Area.objects.get(id = area_id)
    teams = Team.objects.filter(area=area).order_by('name')

    return render(request, 'deployment/ajax_load_teams.html', {'teams': teams})
'''
