from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
from .models import Areas

from inventory.models import Medicine
from deployment.forms import LocationForm, add_location_form
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

def add_location(request):
    form = add_location_form(request.POST or None)
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
        'texthelp': 'Input deployment data here',
        'form': form,
        'actiontype': 'Submit',
        'style':style,
    }
    return render (request, 'deployment/add_location.html', context)

def area_list_view(request):
    areas = Areas.objects.all()
    context = {
        'Title' : 'DOGS AND HANDLERS ASSIGNED FOUs',
        'areas' : areas
    }

    return render(request, 'deployment/area_list.html', context)