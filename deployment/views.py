from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
from .models import Area, Team, Team_Assignment, Current_Deployed
from training.models import K9_Handler
from planningandacquiring.models import K9

from inventory.models import Medicine
from deployment.forms import LocationForm, assign_team_form, AreaForm, TeamForm, assign_current_form
# Create your views here.

def index(request):
    context = {
      'title':'Deployment'
    }
    return render (request, 'deployment/index.html', context)

def deployed_dogs(request):
    context = {
        'title': 'Deployed Dogs',
    }
    return render (request, 'deployment/deployed_dogs.html', context)

def requested_dogs(request):
    context = {
        'title': 'Requested Dogs',
    }
    return render (request, 'deployment/requested_dogs.html', context)

def deploy_number_dogs(request):
    context = {
        'title': 'Deploy Number of Dogs',
    }
    return render (request, 'deployment/deploy_number_dogs.html', context)

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
            form = LocationForm()
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
            form = LocationForm()
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

            Current_Deployed.objects.create(area_id=area1, team_id=team1,
                                            handlers='0', NDD='0', EDD='0', SAR='0')
            style = "ui green message"
            messages.success(request, 'Location has been successfully Added!')
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

    k9_pk = []
    for k9 in team:
        temp = k9.k9
        k9_pk.append(temp.id)

    k9s = K9.objects.filter(pk__in = k9_pk)
    capabilities = []

    for k9 in k9s:
        capabilities.append(k9)

    context = {
        'Title' : 'DOGS AND HANDLERS ASSIGNED FOUs',
        'team_assignment' : team_assignment,
        'current_deployed': current_deployed,
        'team': team,
        'capability': capabilities

    }

    return render(request, 'deployment/area_detail.html', context)
