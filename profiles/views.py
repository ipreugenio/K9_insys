from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login

from profiles.models import User, Personal_Info, Education, Account
from deployment.models import Location
from profiles.forms import add_User_form, add_personal_form, add_education_form, add_user_account

# Create your views here.

def dashboard(request):
    return render (request, 'profiles/dashboard.html')

def profile(request):
    return render (request, 'profiles/profile.html')

def register(request):
    return render (request, 'profiles/register.html')

def login(request):
    style=""

    if request.method == 'POST':
        serial = request.POST['serial_number']
        password = request.POST['password']

        if Account.objects.filter(serial_number=serial).exists():
            if Account.objects.filter(password=password).exists():
                return HttpResponseRedirect('../dashboard')
    else:
        style = "ui red message"
        messages.warning(request, 'Wrong serial number or password!')

    context = {
        'title': "Add User Form",
        'style': style,
    }

    return render (request, 'profiles/login.html', context)

def add_User(request):

    form = add_User_form(request.POST)
    style = ""


    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            new_form = form.save()
            formID = new_form.pk
            request.session["session_userid"] = formID

            '''style = "ui green message"
            messages.success(request, 'User has been successfully Added!')'''

            return HttpResponseRedirect('add_personal_form/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'title': "Add User Form",
        'form': form,
        'style': style,

    }

    return render(request, 'profiles/add_User.html', context)


def add_personal_info(request):
    form = add_personal_form(request.POST)
    style = ""
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            personal_info = form.save(commit=False)
            UserID = request.session["session_userid"]
            user = User.objects.get(id=UserID)
            personal_info.UserID = user
            personal_info.save()
            '''style = "ui green message"
            messages.success(request, 'User has been successfully Added!')'''
            form = add_User_form

            return HttpResponseRedirect('add_education/')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    user = User.objects.get(id=request.session["session_userid"])
    user_name = str(user)
    context = {
        'Title': "Add Personal Information for " + user_name,
        'form': form,
        'style': style,
    }
    print(form)
    return render(request, 'profiles/add_personal_info.html', context)

def add_education(request):
    form = add_education_form(request.POST)
    style = ""
    if request.method == 'POST':

        if form.is_valid():
            personal_info = form.save(commit=False)
            UserID = request.session["session_userid"]
            user = User.objects.get(id=UserID)
            personal_info.UserID = user
            personal_info.save()
            '''style = "ui green message"
            messages.success(request, 'User has been successfully Added!')'''
            form = add_User_form()
            return HttpResponseRedirect('add_user_account/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    user = User.objects.get(id=request.session["session_userid"])
    user_name = str(user)
    context = {
        'Title': "Add Education Information for " + user_name,
        'form': form,
        'style': style,
    }
    print(form)
    return render(request, 'profiles/add_education.html', context)

def add_account(request):
    form = add_user_account(request.POST)
    style = ""
    if request.method == 'POST':

        if form.is_valid():
            account_info = form.save(commit=False)
            UserID = request.session["session_userid"]
            user = User.objects.get(id=UserID)
            account_info.UserID = user
            account_info.save()
            '''style = "ui green message"
            messages.success(request, 'User has been successfully Added!')'''
            return HttpResponseRedirect('../../../../user_add_confirmed/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    user = User.objects.get(id=request.session["session_userid"])
    user_name = str(user)
    context = {
        'Title': "Add Account Information for " + user_name,
        'form': form,
        'style': style,
    }
    print(form)
    return render(request, 'profiles/add_user_account.html', context)

#Listview format
def user_listview(request):
    user = User.objects.all()
    context = {
        'Title' : 'User List',
        'user' : user
    }

    return render(request, 'profiles/user_list.html', context)

#Detailview format
def user_detailview(request, id):
    user = User.objects.get(id = id)
    personal_info = Personal_Info.objects.get(UserID = id)
    education = Education.objects.get(UserID=id)
    account = Account.objects.get(UserID=id)

    context = {
        'Title': 'User Details',
        'user' : user,
        'personal_info': personal_info,
        'education': education,
        'account': account
    }

    return render(request, 'profiles/user_detail.html', context)

#Detailview format
def user_add_confirmed(request):
    return render(request, 'profiles/user_add_confirmed.html')
