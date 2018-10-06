from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages

from profiles.forms import add_User_form
from profiles.models import User

# Create your views here.

def dashboard(request):
    return render (request, 'profiles/dashboard.html')

def profile(request):
    return render (request, 'profiles/profile.html')

def register(request):
    return render (request, 'profiles/register.html')

def login(request):
    return render (request, 'profiles/login.html')

def add_User(request):
    form = add_User_form(request.POST)
    style = ""
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            form.save()

            style = "ui green message"
            messages.success(request, 'K9 has been successfully Added!')
            form = add_User_form()

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'Title': "Add User",
        'form': add_User_form,
        'style': style,
    }

    return render(request, 'profiles/add_User.html', context)