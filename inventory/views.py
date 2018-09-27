from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
# Create your views here.

def index(request):
    return render (request, 'inventory/index.html')

#Medicine
def medicine_add(request):
    return render (request, 'inventory/medicine_add.html')

def medicine_list(request):
    return render (request, 'inventory/medicine_list.html')

#Food
def food_add(request):
    return render (request, 'inventory/food_add.html')

def food_list(request):
    return render (request, 'inventory/food_list.html')

#Equipemnt
def equipment_add(request):
    return render (request, 'inventory/equipment_add.html')

def equipment_list(request):
    return render (request, 'inventory/equipment_list.html')