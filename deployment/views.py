from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
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

    #count deployed dogs
    edd_count = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(k9__capability='EDD').count()
    ndd_count = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(k9__capability='NDD').count()
    sar_count = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(k9__capability='SAR').count()

    #save count
    data.EDD_deployed = edd_count
    data.NDD_deployed = ndd_count
    data.SAR_deployed = sar_count
    data.save()

    #dogs deployed
    dogs_deployed = Team_Dog_Deployed.objects.filter(team_assignment=data)

    if request.method == 'POST':
        checks =  request.POST.getlist('checks') # get the id of all the dogs checked
        #print(checks)

        #get the k9 instance of checked dogs
        checked_dogs = K9.objects.filter(id__in=checks)
        #print(checked_dogs)

        for checked_dogs in checked_dogs:
            Team_Dog_Deployed.objects.create(team_assignment=data, k9=checked_dogs)
            dog = K9.objects.get(id=checked_dogs.id)
            dog.assignment = str(data)
            dog.save()

        style = "ui green message"
        messages.success(request, 'Dogs has been successfully Deployed!')

        return redirect('deployment:team_location_details', id = id)

    context = {
        'title' : data,
        'data' : data,
        'k9' : k9,
        'can_deploy':can_deploy,
        'style': style,
        'dogs_deployed':dogs_deployed,
    }

    return render(request, 'deployment/team_location_details.html', context)

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
    '''k9 = Team_Dog_Deployed.objects.filter(team_assignment=data2)'''
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

    # count deployed dogs
    edd_count = Team_Dog_Deployed.objects.filter(team_requested=data2).filter(k9__capability='EDD').count()
    ndd_count = Team_Dog_Deployed.objects.filter(team_requested=data2).filter(k9__capability='NDD').count()
    sar_count = Team_Dog_Deployed.objects.filter(team_requested=data2).filter(k9__capability='SAR').count()

    # save count
    data2.EDD_deployed = edd_count
    data2.NDD_deployed = ndd_count
    data2.SAR_deployed = sar_count
    data2.save()

    # dogs deployed
    dogs_deployed = Team_Dog_Deployed.objects.filter(team_requested=data2)

    if request.method == 'POST':
        if 'approve' in request.POST:
            data2.status = "Approved"
            data2.save()
            return HttpResponseRedirect('request_dog_list/')
        else:
            data2.request_status = "Denied"
            data2.save()

        checks = request.POST.getlist('checks')  # get the id of all the dogs checked
        # print(checks)

        # get the k9 instance of checked dogs
        checked_dogs = K9.objects.filter(id__in=checks)
        # print(checked_dogs)

        for checked_dogs in checked_dogs:
            Team_Dog_Deployed.objects.create(team_requested=data2, k9=checked_dogs)
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


'''
def location_form(request):
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
        'title': 'Location Form',
        'texthelp': 'Input Location data here',
        'form': form,
        'actiontype': 'Submit',
        'style':style,
    }
    return render (request, 'deployment/location_form.html', context)

def area_form(request):
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
        'title': 'Area Form',
        'texthelp': 'Input Location data here',
        'form': form,
        'actiontype': 'Submit',
        'style':style,
    }
    return render (request, 'deployment/add_location.html', context)

def team_form(request):
    form = TeamForm(request.POST or None)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Team has been successfully Added!')
            form = TeamForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'title': 'Team Form',
        'texthelp': 'Input team data here',
        'form': form,
        'actiontype': 'Submit',
        'style':style,
    }
    return render (request, 'deployment/add_team.html', context)


def assign_team(request):
    form = assign_team_form(request.POST or None)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            area1 = request.POST.get('area')
            team1 = request.POST.get('team')
            handlers1 = request.POST.get('handlers')
            EDD1 = request.POST.get('EDD')
            NDD1 = request.POST.get('NDD')
            SAR1 = request.POST.get('SAR')
            total_dogs1 = (int(EDD1) + int(NDD1) + int(SAR1))

            Team_Assignment.objects.create(area_id=area1, team_id=team1, handlers=handlers1, EDD=EDD1, NDD=NDD1, SAR=SAR1, total_dogs=total_dogs1)

            Current_Deployed.objects.create(area_id=area1, team_id=team1, handlers='0', NDD='0', EDD='0', SAR='0')
            style = "ui green message"
            messages.success(request, 'Location has been successfully Added!')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'title': 'Assign Team Form',
        'texthelp': 'Input assignment data here',
        'form': form,
        'actiontype': 'Submit',
        'style':style,
    }
    return render (request, 'deployment/assign_team.html', context)

def load_teams(request):
    area_id = request.GET.get('area')
    area = Area.objects.get(id = area_id)
    teams = Team.objects.filter(area=area).order_by('name')

    return render(request, 'deployment/ajax_load_teams.html', {'teams': teams})


def area_list_view(request):
    team_assignment = Team_Assignment.objects.all()
    context = {
        'Title' : 'DOGS AND HANDLERS ASSIGNED FOUs',
        'team_assignment' : team_assignment
    }

    return render(request, 'deployment/area_list.html', context)

def area_list_detail(request, id):
    team_assignment = Team_Assignment.objects.get(id = id)
    current_deployed = Current_Deployed.objects.get(id = id)
    team = K9_Handler.objects.all()
    form = DeployDogForm(request.POST or None)
    k9_pk = []
    for k9 in team:
        temp = k9.k9
        k9_pk.append(temp.id)

    k9s = K9.objects.filter(pk__in = k9_pk)
    capabilities = []

    for k9 in k9s:
        capabilities.append(k9)
    #get all Personal_Info
    #pi = Personal_Info.objects.exclude(city=)

    #get all k9, with handler city != to team_assignment city
    #k9 = K9.objects.filter(handler)
    #Personal_Info is where the handler city is referenced

    context = {
        'Title' : 'DOGS AND HANDLERS ASSIGNED FOUs',
        'team_assignment' : team_assignment,
        'current_deployed': current_deployed,
        'team': team,
        'capability': capabilities,
        'form': form
    }

    return render(request, 'deployment/area_detail.html', context)
'''
