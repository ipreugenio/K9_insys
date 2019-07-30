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
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User as AuthUser
from django.db.models import Q

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from profiles.models import User, Personal_Info, Education, Account
from deployment.models import Location, Team_Assignment, Dog_Request, Incidents, Team_Dog_Deployed, Daily_Refresher, Area, K9_Schedule, K9_Pre_Deployment_Items
from deployment.forms import GeoForm, GeoSearch, RequestForm
from profiles.forms import add_User_form, add_personal_form, add_education_form, add_user_account, CheckArrivalForm
from planningandacquiring.models import K9
from django.db.models import Sum
from unitmanagement.models import Equipment_Request, Notification, PhysicalExam
from training.models import Training_Schedule, Training
from inventory.models import Miscellaneous, Food, Medicine_Inventory, Medicine
from django.db.models import Sum

from unitmanagement.models import PhysicalExam, VaccinceRecord, K9_Incident
from datetime import datetime, date
import calendar
import ast
from decimal import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from profiles.serializers import NotificationSerializer, UserSerializer

from deployment.views import load_map, load_locations
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

    # NDD_needed = list(Dog_Request.objects.aggregate(Sum('NDD_needed')).values())[0]
    # EDD_needed = list(Dog_Request.objects.aggregate(Sum('EDD_needed')).values())[0]
    # SAR_needed = list(Dog_Request.objects.aggregate(Sum('SAR_needed')).values())[0]
    #
    # if not NDD_needed:
    #     NDD_needed = 0
    # if not EDD_needed:
    #     EDD_needed = 0
    # if not SAR_needed:
    #     SAR_needed = 0
    #
    # NDD_deployed_request = list(Dog_Request.objects.aggregate(Sum('NDD_deployed')).values())[0]
    # EDD_deployed_request = list(Dog_Request.objects.aggregate(Sum('EDD_deployed')).values())[0]
    # SAR_deployed_request = list(Dog_Request.objects.aggregate(Sum('SAR_deployed')).values())[0]
    #
    # if not NDD_deployed_request:
    #     NDD_deployed_request = 0
    # if not EDD_deployed_request:
    #     EDD_deployed_request = 0
    # if not SAR_deployed_request:
    #     SAR_deployed_request = 0

    k9_demand = NDD_demand + EDD_demand + SAR_demand
    k9_deployed = NDD_deployed + EDD_deployed + SAR_deployed

    # k9_demand_request = NDD_needed + EDD_needed + SAR_needed
    # k9_deployed_request = NDD_deployed_request + EDD_deployed_request + SAR_deployed_request

    unclassified_k9 = K9.objects.filter(capability="None").count()
    untrained_k9 = K9.objects.filter(training_status="Unclassified").count()
    on_training = K9.objects.filter(training_level="Stage 1").count()
    trained = K9.objects.filter(training_status="Trained").count()

    #equipment_requests = Equipment_Request.objects.filter(request_status="Pending").count()

    for_breeding = K9.objects.filter(training_status="For-Breeding").count()

    #Calendar

    events = Dog_Request.objects.all()


    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'can_deploy': can_deploy,
        'k9_demand': k9_demand,
        'k9_deployed': k9_deployed,
        # 'k9_demand_request': k9_demand_request,
        # 'k9_deployed_request': k9_deployed_request,
        'unclassified_k9': unclassified_k9,
        'untrained_k9': untrained_k9,
        'on_training': on_training,
        'trained': trained,
        #'equipment_requests': equipment_requests,
        'for_breeding': for_breeding,

        'events': events,

        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render (request, 'profiles/dashboard.html', context)


#TODO all Team dogs deployed under the team of TL with "Pending status)
def team_leader_dashboard(request):
    user = user_session(request)
    ta = None
    incident_count = 0
    tdd = None
    tdd_count= 0

    form = RequestForm(request.POST or None)
    geoform = GeoForm(request.POST or None)
    geosearch = GeoSearch(request.POST or None)


    k9 = None
    for_arrival = None
    check_arrival = None
    reveal_arrival = False

    try:
        k9 = K9.objects.get(handler = user)
    except:pass

    ta = Team_Assignment.objects.get(team_leader=user)

    incident_count = Incidents.objects.filter(location = ta.location).count()

    tdd = Team_Dog_Deployed.objects.filter(team_assignment=ta).filter(date_pulled = None) #only currently deployed k9s
    tdd_count = tdd.count()

    # NOTE: System checks every nth hours if handler arrival is confirmed, escalate to admin if not confirm (tasks.py)
    for_arrival = tdd.filter(status = "Pending")

    if for_arrival:
        reveal_arrival = True

    print("For arrival")
    print(for_arrival)

    check_arrival = CheckArrivalForm(request.POST or None, for_arrival=for_arrival)

    events = Dog_Request.objects.all()

    year = datetime.now().year
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()

    if request.method == 'POST':
        if form.is_valid():
            checks = geoform['point'].value()
            checked = ast.literal_eval(checks)

            toList = list(checked['coordinates'])

            lon = Decimal(toList[0])
            lat = Decimal(toList[1])

            f = form.save(commit=False)
            f.longtitude = lon
            f.latitude = lat
            f.save()

            messages.success(request, 'Event succesfully saved!')
            return redirect("profiles:team_leader_dashboard")


        if check_arrival.is_valid():

            handlers_arrived_id = check_arrival['team_member'].value()
            print("Handlers Arrived")
            print(handlers_arrived_id)

            handlers_arrived = User.objects.filter(pk__in = handlers_arrived_id)

            for handler in handlers_arrived:
                try:
                    deploy = Team_Dog_Deployed.objects.get(handler = handler)
                    deploy.status = "Deployed"
                    deploy.save()
                except: pass

            #Team Leader

            messages.success(request, 'Arrival succesfully confirmed')
            return redirect("profiles:team_leader_dashboard")
        else:
            print(check_arrival.errors)


    context = {
        'incident_count':incident_count,
        'ta':ta,
        'tdd_count':tdd_count,
        'tdd':tdd,
        'year':year,

        'notif_data':notif_data,
        'count':count,
        'user':user,

        'k9' : k9,
        'form': form,
        'geoform': geoform,
        'geosearch': geosearch,
        'events': events,

        'for_arrival' : for_arrival,
        'check_arrival' : check_arrival,
        'reveal_arrival' : reveal_arrival
    }
    return render (request, 'profiles/team_leader_dashboard.html', context)


# Step 1
# Access this view/function when TL opens dashboard
def check_pre_deployment_items(user):
    all_clear = False
    items_list = [False]

    all_clear = True
    k9 = K9.objects.get(handler = user)


    items_list = []

    collar = False
    vest = False
    leash = False
    shipping_crate = False
    food = False
    vitamins = False
    grooming_kit = False
    first_aid_kit = False
    oral_dextrose = False
    ball = False
    phex = False

    items_list.append(all_clear)

    try:
        checkup = PhysicalExam.objects.filter(dog=k9).latest('id')  # TODO Also check if validity is worth 3 months
        if checkup.cleared == True:
            phex = True
    except: phex = False
    items_list.append((phex, "Physical Exam"))

    agg = Miscellaneous.objects.filter(miscellaneous__contains = "Collar").aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if agg >= 1:
        collar = True
    items_list.append((collar , "Collar"))

    agg = Miscellaneous.objects.filter(miscellaneous__contains = "Vest").aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if  agg >= 1:
        vest = True
    items_list.append((vest , "Vest"))

    agg = Miscellaneous.objects.filter(miscellaneous__contains="Leash").aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if agg >= 1:
        leash = True
    items_list.append((leash , "Leash"))

    agg = Miscellaneous.objects.filter(miscellaneous__contains="Shipping Crate").aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if agg >= 1:
        shipping_crate = True
    items_list.append((shipping_crate , "Shipping Crate"))

    agg = Food.objects.filter(foodtype = "Adult Dog Food").aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if agg >= 1:
        food = True
    items_list.append((food , "Dog Food"))

    medicines = Medicine.objects.filter(med_type = "Vitamins")
    agg = Medicine_Inventory.objects.filter(medicine__in = medicines).aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if agg >= 1:
        vitamins = True
    items_list.append((vitamins , "Vitamins"))

    agg = Miscellaneous.objects.filter(miscellaneous__contains="Grooming Kit").aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if agg >= 1:
        grooming_kit = True
    items_list.append((grooming_kit , "Grooming Kit"))

    agg = Miscellaneous.objects.filter(miscellaneous__contains="First Aid Kit").aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if agg >= 1:
        first_aid_kit = True
    items_list.append((first_aid_kit , "First Aid Kit"))

    agg = Miscellaneous.objects.filter(miscellaneous__contains="Oral Dextrose").aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if agg >= 1:
        oral_dextrose = True
    items_list.append((oral_dextrose , "Oral Dextrose"))

    agg = Miscellaneous.objects.filter(miscellaneous__contains="Ball").aggregate(Sum('quantity'))
    agg = agg['quantity__sum']
    if agg is None:
        agg = 0
    if agg >= 1:
        ball = True
    items_list.append((ball , "Ball"))

    #Check if items are complete

    check_list = [collar, vest, leash, shipping_crate, food, vitamins, grooming_kit, first_aid_kit, oral_dextrose, ball, phex]

    for item in check_list:
        if item == False:
            all_clear = False

    items_list[0] = all_clear

    return items_list


#Step 2
#Handler confirms items and will be part of the team officially deployed
def confirm_pre_deployment_items(request, k9):

    pre_deployment_items = K9_Pre_Deployment_Items.objects.get(k9=k9)
    pre_deployment_items.status = "Confirmed"
    pre_deployment_items.save()

    return False

def handler_dashboard(request):

    user = user_session(request)
    form = RequestForm(request.POST or None)
    geoform = GeoForm(request.POST or None)
    geosearch = GeoSearch(request.POST or None)

    
    dr = 0
    k9 = None
    training_sched = None
    training = None

    pre_deployment_items = False
    all_clear = False
    reveal_items = False


    k9 = K9.objects.get(handler=user)
    today = datetime.today()

    items_list = []
    if k9.training_status == "For-Deployment":

        items_list = check_pre_deployment_items(user)
        all_clear = items_list[0]

        del items_list[0]

        print("Items List")
        print(items_list)

        pre_deployment_items = K9_Pre_Deployment_Items.objects.get(k9=k9)
        initial_sched = pre_deployment_items.initial_sched

        delta = initial_sched.date_start - today.date()
        if delta.days <= 7 and k9.training_status == "For-Deployment" and pre_deployment_items.status == "Pending": #1 week before deployment
            reveal_items = True


    # TODO try except for when handler does not yet have a k9
    # TODO try except for when k9s still don't have a skill
    # TODO try except when k9 has finished training

    try:
        training = Training.objects.get(k9=k9, training=k9.capability)
        training_sched = Training_Schedule.objects.filter(stage=training.stage).get(k9=k9)
    except: pass


    print("ALL CLEAR")
    print(all_clear)
    print("REVEAL ITEMS")
    print(reveal_items)

    drf = Daily_Refresher.objects.filter(handler=user).filter(date=datetime.now())

    if drf.exists():
        dr = 1
    else:
        dr = 0

    show_start = False
    show_end = False

    if request.method == 'POST':
        start_training = request.POST.get('start_training')
        end_training = request.POST.get('end_training')

        confirm_deployment = request.POST.get('confirm_deployment')
        if confirm_deployment:
            confirm_pre_deployment_items(request, k9)
            return redirect("profiles:handler_dashboard")

        if start_training:
            print("START TRAINING VALUE")
            print(start_training)

            try:
                training_sched.date_start = today
                training_sched.save()
            except: pass
        if end_training:
            print("END TRAINING VALUE")
            print(end_training)

            try:
                training_sched.date_end = today
                training_sched.save()
            except: pass

        if form.is_valid():
            checks = geoform['point'].value()
            checked = ast.literal_eval(checks)
           
            toList = list(checked['coordinates'])
          
            lon = Decimal(toList[0])
            lat = Decimal(toList[1])

            f = form.save(commit=False)
            f.longtitude = lon
            f.latitude = lat
            f.save()

            messages.success(request, 'event')
            return redirect("profiles:handler_dashboard")

    events = Dog_Request.objects.all()

    try:
        if training_sched.date_start is None and training_sched.date_end is None:
            show_start = True

        elif training_sched.date_start is not None and training_sched.date_end is None:
            show_end = True

        elif training_sched.date_start is not None and training_sched.date_end is not None:
            show_start = True
            show_end = True

        else:
                pass
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
        'form': form,
        'geoform': geoform,
        'geosearch': geosearch,
        'events': events,

        'show_start': show_start,
        'show_end': show_end,
        'training_sched' : training_sched,

        'pre_deployment_item' : pre_deployment_items,
        'reveal_items' : reveal_items,
        'all_clear' : all_clear,
        'items_list' : items_list
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

def commander_dashboard(request):
    user = user_session(request)
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'profiles/commander_dashboard.html', context)

def operations_dashboard(request):
    user = user_session(request)
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'profiles/operations_dashboard.html', context)

def trainer_dashboard(request):
    user = user_session(request)
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'profiles/trainer_dashboard.html', context)

def profile(request):
   
    # first_day = datetime.date.today().replace(day=1)
    # last_day = datetime.date.today().replace(day=calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1])

    # print(first_day, last_day)
    # phex = PhysicalExam.objects.filter(date_next_exam__range=[first_day, last_day])
    # vac = VaccinceRecord.objects.filter(date_validity__range=[first_day, last_day])
    # list = zip(phex,vac)
    today = datetime.today()

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

def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect('profiles:login')

def login(request):
    if request.method == 'POST':
        serial = request.POST['serial_number']
        password = request.POST['password']
        user_auth = authenticate(request, username=serial, password=password)
        print(password)
        if user_auth is not None:
            auth_login(request, user_auth)
            request.session["session_serial"] = serial
            account = Account.objects.get(serial_number = serial)
            user = User.objects.get(id = account.UserID.id) 

            request.session["session_user_position"] = user.position
            request.session["session_id"] = user.id
            request.session["partnered"] = user.partnered
            request.session["session_username"] = str(user)

            print(request.session["partnered"])
            #TRAINOR, OPERATIONS
            if user.position == 'Aministrator':
                return HttpResponseRedirect('../dashboard')
            elif user.position == 'Veterinarian':
                return HttpResponseRedirect('../vet-dashboard')
            elif user.position == 'Team Leader':
                return HttpResponseRedirect('../team-leader-dashboard')
            elif user.position == 'Handler':
                return HttpResponseRedirect('../handler-dashboard')
            elif user.position == 'Commander':
                return HttpResponseRedirect('../commander-dashboard')
            elif user.position == 'Operations':
                return HttpResponseRedirect('../operations-dashboard')
            elif user.position == 'Trainer':
                return HttpResponseRedirect('../trainer-dashboard')

            else:
                return HttpResponseRedirect('../dashboard')
        else:
            messages.warning(request, 'username or password is invalid!')

    return render (request, 'profiles/login.html')

def add_User(request):

    form = add_User_form(request.POST, request.FILES)
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

            return HttpResponseRedirect('../../../../user_list/')

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
    style = "ui green message"

    if request.method == 'POST':
        date = request.POST.get('date_input')
        status = request.POST.get('status_input')
        handler_id = request.POST.get('id_input')

        u = User.objects.get(id=handler_id)
        u.retire_quit_died = date
        u.partnered = False
        u.assigned = False

        if status == 'Quit':
            u.status = 'No Longer Employed'

        u.save()

        try:
            k = K9.objects.get(handler=u) 
            k.handler = None
            k.save()
        except:
            pass

        messages.success(request, 'User status has been updated to '+ u.status +'!')
        

    context = {
        'Title' : 'User List',
        'style':style,
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



class ScheduleView(APIView):
    def get(self, request, format=None):
        user = user_session(request)

        today = datetime.now()
        print(date.today())

        k9 = K9.objects.get(handler=user)
        sched = K9_Schedule.objects.filter(k9=k9).filter(date_end__gte= today)

        sched_items = []

        for items in sched:
            i = [items.dog_request.location, items.date_start, items.date_end]
            sched_items.append(i)

        data = {
            "sched_items":sched_items,
        }
        return Response(data)

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

def update_event(request):

    event = None

    event_id = request.GET.get('event_id')
    event_start = request.GET.get('event_start')
    event_end = request.GET.get('event_end')
    event_title = request.GET.get('event_title')
    event_allDay = request.GET.get('event_allDay')
    event_allDay = event_allDay.capitalize()
    python_date_start = datetime.fromtimestamp(int(event_start))
    if event_end is not None:
        python_date_end = datetime.fromtimestamp(int(event_end))
        # if python_date_start.day == python_date_end.day:
        #     python_date_end = python_date_end + relativedelta.relativedelta(days=1)
    else:
        python_date_end = python_date_start
        #python_date_end = python_date_end + relativedelta.relativedelta(days=1)


    print("ID : " + event_id)
    print("TITLE : " + event_title)
    print("START : " + str(python_date_start))
    print("END : " + str(python_date_end))
    print("ALLDAY : " + event_allDay)

    event = Events.objects.get(id=event_id)
    event.event_name = event_title
    event.start_date = python_date_start
    event.end_date = python_date_end

    event.all_day = event_allDay
    event.save()


    context = {"event": event}

    return render(request, 'module/something.html', context)

class UserView(viewsets.ModelViewSet):
    queryset = AuthUser.objects.all()
    serializer_class = UserSerializer
