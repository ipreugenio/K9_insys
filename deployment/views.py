from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages

from inventory.models import Medicine
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