from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User as AuthUser
from django.db.models import Q

from profiles.models import User, Personal_Info, Education, Account
from deployment.models import Location, Team_Assignment, Dog_Request, Incidents, Team_Dog_Deployed, Daily_Refresher, Area
from profiles.forms import add_User_form, add_personal_form, add_education_form, add_user_account
from planningandacquiring.models import K9
from django.db.models import Sum
from unitmanagement.models import Equipment_Request, Notification

from unitmanagement.models import PhysicalExam, VaccinceRecord, K9_Incident
from datetime import datetime
import calendar

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from profiles.serializers import NotificationSerializer, UserSerializer
# Create your views here.

def notif(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)
    
    if user_in_session.position == 'Veterinarian':
        notif = Notification.objects.filter(position='Veterinarian').order_by('-datetime')
    elif user_in_session.position == 'Handler':
        notif = Notification.objects.filter(user=user_in_session).order_by('-datetime')
    else:
        notif = Notification.objects.filter(position='Administrator').order_by('-datetime')
   
    return notif

def notif_list(request):

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context={
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'profiles/notification_list.html', context)

def user_session(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)
    return user_in_session

@login_required
def dashboard(request):
    user = user_session(request)

    can_deploy = K9.objects.filter(training_status='For-Deployment').filter(assignment='None').count()
    NDD_count = K9.objects.filter(capability='NDD').count()
    EDD_count = K9.objects.filter(capability='EDD').count()
    SAR_count = K9.objects.filter(capability='SAR').count()

    NDD_deployed = list(Team_Assignment.objects.aggregate(Sum('NDD_deployed')).values())[0]
    EDD_deployed = list(Team_Assignment.objects.aggregate(Sum('EDD_deployed')).values())[0]
    SAR_deployed = list(Team_Assignment.objects.aggregate(Sum('SAR_deployed')).values())[0]

    if not NDD_deployed:
        NDD_deployed = 0
    if not EDD_deployed:
        EDD_deployed = 0
    if not SAR_deployed:
        SAR_deployed = 0

    NDD_demand = list(Team_Assignment.objects.aggregate(Sum('NDD_demand')).values())[0]
    EDD_demand = list(Team_Assignment.objects.aggregate(Sum('EDD_demand')).values())[0]
    SAR_demand = list(Team_Assignment.objects.aggregate(Sum('SAR_demand')).values())[0]

    if not NDD_demand:
        NDD_demand = 0
    if not EDD_demand:
        EDD_demand = 0
    if not SAR_demand:
        SAR_demand = 0

    NDD_needed = list(Dog_Request.objects.aggregate(Sum('NDD_needed')).values())[0]
    EDD_needed = list(Dog_Request.objects.aggregate(Sum('EDD_needed')).values())[0]
    SAR_needed = list(Dog_Request.objects.aggregate(Sum('SAR_needed')).values())[0]

    if not NDD_needed:
        NDD_needed = 0
    if not EDD_needed:
        EDD_needed = 0
    if not SAR_needed:
        SAR_needed = 0

    NDD_deployed_request = list(Dog_Request.objects.aggregate(Sum('NDD_deployed')).values())[0]
    EDD_deployed_request = list(Dog_Request.objects.aggregate(Sum('EDD_deployed')).values())[0]
    SAR_deployed_request = list(Dog_Request.objects.aggregate(Sum('SAR_deployed')).values())[0]

    if not NDD_deployed_request:
        NDD_deployed_request = 0
    if not EDD_deployed_request:
        EDD_deployed_request = 0
    if not SAR_deployed_request:
        SAR_deployed_request = 0

    k9_demand = NDD_demand + EDD_demand + SAR_demand
    k9_deployed = NDD_deployed + EDD_deployed + SAR_deployed

    k9_demand_request = NDD_needed + EDD_needed + SAR_needed
    k9_deployed_request = NDD_deployed_request + EDD_deployed_request + SAR_deployed_request

    unclassified_k9 = K9.objects.filter(capability="None").count()
    untrained_k9 = K9.objects.filter(training_status="Unclassified").count()
    on_training = K9.objects.filter(training_level="Stage 1").count()
    trained = K9.objects.filter(training_status="Trained").count()

    equipment_requests = Equipment_Request.objects.filter(request_status="Pending").count()

    for_breeding = K9.objects.filter(training_status="For-Breeding").count()

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'can_deploy': can_deploy,
        'k9_demand': k9_demand,
        'k9_deployed': k9_deployed,
        'k9_demand_request': k9_demand_request,
        'k9_deployed_request': k9_deployed_request,
        'unclassified_k9': unclassified_k9,
        'untrained_k9': untrained_k9,
        'on_training': on_training,
        'trained': trained,
        'equipment_requests': equipment_requests,
        'for_breeding': for_breeding,

        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render (request, 'profiles/dashboard.html', context)

def team_leader_dashboard(request):
    user = user_session(request)
    ta = None
    incident_count = 0
    tdd = None
    tdd_count= 0
    try:
        ta = Team_Assignment.objects.get(team_leader=user)

        incident_count = Incidents.objects.filter(location = ta.location).count()

        tdd_count = Team_Dog_Deployed.objects.filter(team_assignment=ta).filter(status='Deployed').count()
        tdd = Team_Dog_Deployed.objects.filter(team_assignment=ta).filter(status='Deployed')
    except:
        pass

    year = datetime.now().year
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()

    context = {
        'incident_count':incident_count,
        'ta':ta,
        'tdd_count':tdd_count,
        'tdd':tdd,
        'year':year,

        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'profiles/team_leader_dashboard.html', context)

def commander_dashboard(request):
    user = user_session(request)
    
    dr = 0
    area = None
    try:
        area = Location.objects.filter(area__commander=user).count()
     
    except:
        pass
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'area':area,
    }
    return render (request, 'profiles/commander_dashboard.html', context)

def handler_dashboard(request):
    user = user_session(request)
    
    dr = 0
    k9 = None
    try:
        k9 = K9.objects.get(handler=user)
        drf = Daily_Refresher.objects.filter(handler=user).filter(date=datetime.now())
        if drf.exists():
            dr = 1
        else:
            dr = 0
    except:
        pass
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'k9':k9,
        'dr':dr,
    }
    return render (request, 'profiles/handler_dashboard.html', context)

def vet_dashboard(request):
    user = user_session(request)
    
    cv1 = VaccinceRecord.objects.filter(dhppil_cv_1=False).count() #dhppil_cv_1
    cv2 = VaccinceRecord.objects.filter(dhppil_cv_2=False).count() #dhppil_cv_2
    cv3 = VaccinceRecord.objects.filter(dhppil_cv_3=False).count() #dhppil_cv_3

    rabies = VaccinceRecord.objects.filter(anti_rabies=False).count() #anti_rabies
    
    bd1 = VaccinceRecord.objects.filter(bordetella_1=False).count() #bordetella_1
    bd2 = VaccinceRecord.objects.filter(bordetella_2=False).count() #bordetella_2

    dh1 = VaccinceRecord.objects.filter(dhppil4_1=False).count() #dhppil4_1
    dh2 = VaccinceRecord.objects.filter(dhppil4_2=False).count() #dhppil4_2

    adoption = K9.objects.filter(training_status='For-Adoption').count()

    vac_pending = VaccinceRecord.objects.filter(Q(dhppil_cv_1=False) | Q(dhppil_cv_2=False) | Q(dhppil_cv_3=False) | Q(anti_rabies=False) | Q(bordetella_1=False) | Q(bordetella_2=False) | Q(dhppil4_1=False) | Q(dhppil4_2=False)).count()
    
    #TODO Physical Exam
    # phex_pending = 
    health_pending = K9_Incident.objects.filter(incident='Sick').filter(status='Pending').count()

    # pending incidents
    incident =  K9_Incident.objects.filter(incident='Accident').filter(status='Pending').count()
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'vac_pending':vac_pending,
        'health_pending':health_pending,
        'cv1':cv1,
        'cv2':cv2,
        'cv3':cv3,
        'rabies':rabies,
        'bd1':bd1,
        'bd2':bd2,
        'dh1':dh1,
        'dh2':dh2,
        'incident':incident,
    }
    return render (request, 'profiles/vet_dashboard.html', context)

def profile(request):
   
    first_day = datetime.date.today().replace(day=1)
    last_day = datetime.date.today().replace(day=calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1])

    # print(first_day, last_day)
    # phex = PhysicalExam.objects.filter(date_next_exam__range=[first_day, last_day])
    # vac = VaccinceRecord.objects.filter(date_validity__range=[first_day, last_day])
    # list = zip(phex,vac)
    today = datetime.date.today()

    serial = request.session['session_serial']
    print(serial)
    
    account = Account.objects.get(serial_number=serial)
    user = User.objects.get(id = account.UserID.id)
    p_info = Personal_Info.objects.get(UserID=user) 
    e_info = Education.objects.get(UserID=user)

    print(account.UserID.position)

    uform = add_User_form(request.POST or None,  request.FILES or None, instance = user)
    pform = add_personal_form(request.POST or None, instance = p_info)
    eform = add_education_form(request.POST or None, instance = e_info)

    if request.method == 'POST':
        print(uform.errors)
        if uform.is_valid():
            print(pform.errors)
            if pform.is_valid():
                print(eform.errors)
                if eform.is_valid():
                    if uform.status == 'No Longer Employed':
                        uform.partnered = False
                        try:
                            k9 = K9.objects.get(handler=uform)
                            k9.handler = None
                            k9.save()
                        except:
                            pass

                    uform.save()
                    pform.save()
                    eform.save()
                    messages.success(request, 'Your Profile has been successfully Updated!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    
    context={
        # 'phex': phex,
        # 'vac': vac,
        # 'list': list,
        'today': today,
        'uform':uform,
        'pform': pform,
        'eform': eform,
        'user':user,
        'notif_data':notif_data,
        'count':count,
    }
    return render (request, 'profiles/profile.html', context)

def register(request):
    return render (request, 'profiles/register.html')


def home(request):
    id = request.user.id

    print(id)
    user = User.objects.get(id =id)


    request.session["session_serial"] = request.user.username
    request.session["session_user_position"] = user.position
    request.session["session_id"] = user.id
    request.session["session_username"] = str(user)

    if user.position == 'Team Leader':
        return HttpResponseRedirect('../team-leader-dashboard')
    elif user.position == 'Handler':
        return HttpResponseRedirect('../handler-dashboard')
    elif user.position == 'Veterinarian':
        return HttpResponseRedirect('../vet-dashboard')
    else:
        return HttpResponseRedirect('../dashboard')



    return redirect('profiles:vet_dashboard')


def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    auth_logout(request)
    return redirect('profiles:login')

def login(request):
    if request.method == 'POST':
        serial = request.POST['serial_number']
        password = request.POST['password']
        user_auth = authenticate(request, username=serial, password=password)
        print(user_auth)
        if user_auth is not None:
            auth_login(request, user_auth)
            request.session["session_serial"] = serial
            account = Account.objects.get(serial_number = serial)
            user = User.objects.get(id = account.UserID.id)

            request.session["session_user_position"] = user.position
            request.session["session_id"] = user.id
            request.session["session_username"] = str(user)

            if user.position == 'Aministrator':
                return HttpResponseRedirect('../dashboard')
            elif user.position == 'Veterinarian':
                return HttpResponseRedirect('../vet-dashboard')
            elif user.position == 'Team Leader':
                return HttpResponseRedirect('../team-leader-dashboard')
            elif user.position == 'Handler':
                return HttpResponseRedirect('../handler-dashboard')
            else:
                return HttpResponseRedirect('../dashboard')

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

            '''style = "ui green message"
            messages.success(request, 'User has been successfully Added!')'''

            return HttpResponseRedirect('add_personal_form/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Add User Form",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
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
            user_s = User.objects.get(id=UserID)
            personal_info.UserID = user_s
            personal_info.save()
            '''style = "ui green message"
            messages.success(request, 'User has been successfully Added!')'''
            form = add_User_form

            return HttpResponseRedirect('add_education/')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    user_s = User.objects.get(id=request.session["session_userid"])
    user_name = str(user_s)
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Add Personal Information for " + user_name,
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
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
            user_s = User.objects.get(id=UserID)
            personal_info.UserID = user_s
            personal_info.save()
            '''style = "ui green message"
            messages.success(request, 'User has been successfully Added!')'''
            form = add_User_form()
            return HttpResponseRedirect('add_user_account/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    user_s = User.objects.get(id=request.session["session_userid"])
    user_name = str(user_s)
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Add Education Information for " + user_name,
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    print(form)
    return render(request, 'profiles/add_education.html', context)

def add_account(request):
    form = add_user_account(request.POST or None)
    style = ""

    UserID = request.session["session_userid"]
    data = User.objects.get(id = UserID)

    if request.method == 'POST':
        if form.is_valid():
            form = form.save(commit=False)
            form.username = 'O-' + str(data.id) 
            form.first_name = data.firstname
            form.last_name = data.lastname
            form.save()

            return HttpResponseRedirect('../../../../user_add_confirmed/')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Add Account Information for " + data.fullname,
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render(request, 'profiles/add_user_account.html', context)

#Listview format
def user_listview(request):
    user_s = User.objects.all()
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title' : 'User List',
        'user_s' : user_s,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'profiles/user_list.html', context)

#Detailview format
def user_detailview(request, id):
    user_s = User.objects.get(id = id)
    personal_info = Personal_Info.objects.get(UserID = id)
    education = Education.objects.get(UserID=id)
    account = Account.objects.get(UserID=id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': 'User Details',
        'user_s' : user_s,
        'personal_info': personal_info,
        'education': education,
        'account': account,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'profiles/user_detail.html', context)

#Detailview format
def user_add_confirmed(request):
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render(request, 'profiles/user_add_confirmed.html', context)

#TODO
class NotificationListView(APIView):

    def get(self, request):
        user_serial = request.session['session_serial']
        user = Account.objects.get(serial_number=user_serial)
        current_user = User.objects.get(id=user.UserID.id)

        #TODO
        if current_user.position == 'Handler':
            k9 = K9.objects.get(handler=current_user)  
            notif = Notification.objects.filter(k9=k9)
        else:
            notif = Notification.objects.filter(position=current_user.position)
        
        serializer = NotificationSerializer(notif, many=True)
        return Response(serializer.data)

    def put(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationDetailView(APIView):
    def get(self, request, id):
        notif = get_object_or_404(Notification, id=id)
        serializer = NotificationSerializer(notif)
        return Response(serializer.data)

    def delete(self, request, id):
        notif = get_object_or_404(Notification, id=id)
        notif.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class UserView(viewsets.ModelViewSet):
#     queryset = AuthUser.objects.all()
#     serializer_class = UserSerializer
