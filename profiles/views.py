from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
# Create your views here.

def dashboard(request):
    return render (request, 'profiles/dashboard.html')

def profile(request):
    return render (request, 'profiles/profile.html')

def register(request):
    return render (request, 'profiles/register.html')

def login(request):
    return render (request, 'profiles/login.html')