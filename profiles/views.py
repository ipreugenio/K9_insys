from django.http import HttpResponse, HttpResponseRedirect
from .forms import add_User_form, add_personal_form
from .models import Users
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
from django.contrib.sessions.models import Session
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
            new_form = form.save()

            formID = new_form.pk
            request.session["session_userid"] = formID


            style = "ui green message"
            messages.success(request, 'User has been successfully Added!')
            form = add_User_form()

            return redirect('add_personal_info.html')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'Title': "Add User",
        'form': add_User_form,
        'style': style,

    }

    '''if form.is_valid():
        return redirect('add_personal_info')
    else:
        return render(request, 'profiles/add_User.html', context)'''


def add_personal_info(request):
    form = add_personal_form(request.POST)
    style = ""
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            personal_info = form.save(commit=False)
            personal_info.UserID = request.session["session_userid"]
            personal_info.save()
            style = "ui green message"
            messages.success(request, 'User has been successfully Added!')
            form = add_User_form
            user = Users.objects.get(id = request.session["session_userid"])
            user_name = str(user.Name)
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'Title': "Add Personal Information for " + user_name,
        'form': add_personal_form,
        'style': style,
    }

    return render(request, 'profiles/add_personal_info.html', context)