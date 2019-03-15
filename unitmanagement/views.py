from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
import datetime as dt
from datetime import timedelta, date
from decimal import Decimal
from django.db.models import Sum, Avg, Max
from django.core.exceptions import ObjectDoesNotExist

from planningandacquiring.models import K9
from unitmanagement.models import PhysicalExam, Health, HealthMedicine, K9_Incident, Handler_Incident, K9_Incident
from unitmanagement.forms import PhysicalExamForm, HealthForm, HealthMedicineForm, VaccinationRecordForm, RequestForm, HandlerOnLeaveForm
from unitmanagement.forms import K9IncidentForm, HandlerIncidentForm, VaccinationUsedForm, ReassignAssetsForm, ReproductiveForm
from inventory.models import Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Miscellaneous_Subtracted_Trail
from inventory.models import Medicine_Received_Trail, Food_Subtracted_Trail, Food
from unitmanagement.models import HealthMedicine, Health, VaccinceRecord, Requests, VaccineUsed, Notification
from deployment.models import K9_Schedule, Dog_Request, Team_Dog_Deployed
from profiles.models import User, Account, Personal_Info
from training.models import K9_Handler

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from unitmanagement.serializers import K9Serializer, UserSerializer

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

def currrent_user(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)
    return user_in_session

def user_session(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)
    return user_in_session

#TODO REDIRECT
def redirect_notif(request, id):
    notif = Notification.objects.get(id=id)
    if notif.notif_type == 'physical_exam':
        notif.viewed = True
        notif.save()
        request.session['phex_k9_id'] = notif.k9.id
        return redirect('unitmanagement:physical_exam_form')
    elif notif.notif_type == 'vaccination':
        notif.viewed = True
        notif.save()
        return redirect('unitmanagement:health_history', id = notif.k9.id)
    elif notif.notif_type == 'dog_request':
        notif.viewed = True
        notif.save()
        return redirect('deployment:request_dog_details', id = notif.other_id)
    elif notif.notif_type == 'inventory_low':
        notif.viewed = True
        notif.save()
        return redirect('inventory:food_inventory_list')
    elif notif.notif_type == 'heat_cycle':
        notif.viewed = True
        notif.save()
        return redirect('unitmanagement:reproductive_edit', id = notif.k9.id)
    elif notif.notif_type == 'k9_sick' :
        notif.viewed = True
        notif.save()
        return redirect('unitmanagement:k9_sick_details', id = notif.other_id)
    elif notif.notif_type == 'k9_died' :
        notif.viewed = True
        notif.save()
        return redirect('planningandacquiring:K9_detail', id = notif.k9.id)
    elif notif.notif_type == 'handler_died' :
        notif.viewed = True
        notif.save()
        return redirect('profiles:user_detail', id = notif.user.id)
    elif notif.notif_type == 'equipment_request' :
        notif.viewed = True
        notif.save()
        return redirect('unitmanagement:change_equipment', id = notif.other_id)
    #TODO location incident view details 
    # elif notif.notif_type == 'location_incident' :
    #     notif.viewed = True
    #     notif.save()
    #     return redirect('deployment:incident_detail', id = notif.other_id)
    

def index(request):

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }        

    return render (request, 'unitmanagement/index.html', context)

#TODO Formset does not got to db
#INITIALIZE HEALTH FORM AND PHYSICAL FORM
def health_form(request):
    medicine_formset = inlineformset_factory(Health, HealthMedicine, form=HealthMedicineForm, extra=1, can_delete=True)
    style=""
    form = HealthForm(request.POST or None)

    if request.method == "POST":
        #print(form)
        if form.is_valid():
            new_form = form.save()
            new_form = new_form.pk
            print('Form_id: ', new_form)
            form_instance = Health.objects.get(id=new_form)

            #Get K9
            print('from form: ', form_instance.dog)

            dog = K9.objects.get(id=form_instance.dog.id)
            print('from query ', dog)
            
            print(request.session['problem'])
            #Use Health form instance for Health Medicine
            formset = medicine_formset(request.POST, instance=form_instance)
            form_med = []
            form_quantity = []
            inventory_quantity = []
            insufficient_quantity = []
            insufficient_med = []
            days = []
            
            msg = 'Insuficient quantity! Availability for '

            if formset.is_valid():
                for form in formset:
                    m = Medicine.objects.get(medicine_fullname= form.cleaned_data['medicine'])
                    form_med.append(m)
                    form_quantity.append(form.cleaned_data['quantity'])
                    days.append(form.cleaned_data['duration'])
                    print(form_quantity)

                mi = Medicine_Inventory.objects.filter(medicine__in=form_med)
                
                for mi in mi:
                    inventory_quantity.append(mi.quantity)

                ctr1 = 0
                ctr2 = len(form_quantity)
                # for mi in mi:
                #     if mi.quantity >= form_quantity[i]
                #     i
                while ctr1 < ctr2:
                    if inventory_quantity[ctr1] >= form_quantity[ctr1]:
                        pass
                    else:
                        insufficient_quantity.append(inventory_quantity[ctr1])
                        insufficient_med.append(form_med[ctr1])
                    ctr1=ctr1+1

                print('form_med:', form_med)
                print('form_quantity:', form_quantity)
                print('inventory_med:', insufficient_med)
                print('inventory_quantity:', insufficient_quantity)
                print('Duration:', max(days))

                form_instance.duration = max(days)
                form_instance.save()

                ctr3 = len(insufficient_med)
                ctr4=0

                if ctr3 != 0:
                    while ctr4 < ctr3:
                        if ctr4 == ctr3-1:
                            msg = msg + str(insufficient_med[ctr4]) + ':' + str(insufficient_quantity[ctr4]) + 'pcs.'
                        else:
                            msg = msg + str(insufficient_med[ctr4]) + ':' + str(insufficient_quantity[ctr4]) + 'pcs, '
                        ctr4=ctr4+1
                    form_instance.delete()
                    style = "ui red message"
                    messages.warning(request, msg)
                    
                else:
                    for form in formset:
                        form.save()
                    dog.status = 'Sick'
                    style = "ui green message"
                    messages.success(request, 'Health Form has been successfully recorded!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Health Form",
        'form':HealthForm,
        'formset':medicine_formset(),
        'actiontype': "Submit",
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/health_form.html', context)

#TODO MAKE INITIAL VALUE OF DOG 
def physical_exam_form(request):
    form = PhysicalExamForm(request.POST or None)
    user_serial = request.session['session_serial']
    user_s = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user_s.UserID.id)

    if 'phex_k9_id' in request.session:
        form.initial['dog'] = K9.objects.get(id=request.session['phex_k9_id'])
    
    style=""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            new_form = form.save()
            new_form.date_next_exam = dt.date.today() + dt.timedelta(days=365)

            new_form.user = current_user
            new_form.save()

            style = "ui green message"
            messages.success(request, 'Physical Exam has been successfully recorded!')
            form = PhysicalExamForm()

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Physical Exam",
        'actiontype': "Submit",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/physical_exam_form.html', context)

def health_record(request):
    position = request.session["session_user_position"]

    if position == "Handler":
        serial = request.session["session_serial"]

        number = Account.objects.get(serial_number=serial)
        handler = User.objects.get(id=number.UserID.id)
        k9 = K9_Handler.objects.get(handler_id=handler.id)
        data = K9.objects.get(id = int(k9.id))

    elif position == "Veterinarian":
        data = K9.objects.all()


    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Health Record",
        'actiontype': "Submit",
        'data': data,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/health_record.html', context)

def health_history(request, id):
    user_serial = request.session['session_serial']
    user_s = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user_s.UserID.id)


    data = K9.objects.get(id=id)
    health_data = Health.objects.filter(dog = data).order_by('-date')
    phyexam_data = PhysicalExam.objects.filter(dog = data).order_by('-date')

    vaccine_record = VaccinceRecord.objects.get(k9 = data)
    dtoday = dt.date.today()

    vaccine_record_form = VaccinationRecordForm(request.POST or None, instance = vaccine_record)
    vaccine_used_form = VaccinationUsedForm(request.POST or None)
    vaccines = Medicine.objects.filter(med_type = "Vaccine").order_by('medicine')
    vaccine_available = Medicine_Inventory.objects.filter(medicine__in = vaccines).exclude(quantity=0)
   
    active_1 = ' active'
    active_2 = ''
    active_3 = ''
    style='ui green message'

    # GET DOG AGE
    # 2weeks=14days, 4Weeks=28days, 6weeks=42days, 8Weeks=56days, 9weeks=63days, 10weeks=70days
    # 14weeks=98days, 15weeks=105days, 16weeks=112days, 18weeks=126days, 20weeks=140days, 22weeks=154days
    # 24weeks=168days, 26weeks=183days, 28weeks=196days, 30weeks=210days, 32weeks=224days, 34weeks=238days
    dog_days =  dtoday - data.birth_date

    data_deworming_1 = ''
    data_deworming_2 = ''
    data_deworming_3 = ''
    data_dhppil_cv_1 = ''
    data_heartworm_1 = ''
    data_bordetella_1 = ''
    data_tick_flea_1 = ''
    data_dhppil_cv_2 = ''
    data_deworming_4 = ''
    data_heartworm_2 = ''
    data_bordetella_2 = ''
    data_anti_rabies = ''
    data_tick_flea_2 = ''
    data_dhppil_cv_3 = ''
    data_heartworm_3 = ''
    data_dhppil4_1 = ''
    data_tick_flea_3 = ''
    data_dhppil4_2 = ''
    data_heartworm_4 = ''
    data_tick_flea_4 = ''
    data_heartworm_5 = ''
    data_tick_flea_5 = ''
    data_heartworm_6 = ''
    data_tick_flea_6 = ''
    data_heartworm_7 = ''
    data_tick_flea_7 = ''
    data_heartworm_8 = ''


    #data of vaccines used
    if data.source == 'Breeding':
        data_deworming_1 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='deworming_1')
        data_deworming_2 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='deworming_2')
        data_deworming_3 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='deworming_3')
        data_dhppil_cv_1 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='dhppil_cv_1')
        data_heartworm_1 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='heartworm_1')
        data_bordetella_1 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='bordetella_1')
        data_tick_flea_1 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='tick_flea_1')
        data_dhppil_cv_2 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='dhppil_cv_2')
        data_deworming_4 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='deworming_4')
        data_heartworm_2 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='heartworm_2')
        data_bordetella_2 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='bordetella_2')
        data_anti_rabies = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='anti_rabies')
        data_tick_flea_2 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='tick_flea_2')
        data_dhppil_cv_3 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='dhppil_cv_3')
        data_heartworm_3 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='heartworm_3')
        data_dhppil4_1 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='dhppil4_1')
        data_tick_flea_3 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='tick_flea_3')
        data_dhppil4_2 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='dhppil4_2')
        data_heartworm_4 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='heartworm_4')
        data_tick_flea_4 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='tick_flea_4')
        data_heartworm_5 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='heartworm_5')
        data_tick_flea_5 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='tick_flea_5')
        data_heartworm_6 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='heartworm_6')
        data_tick_flea_6 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='tick_flea_6')
        data_heartworm_7 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='heartworm_7')
        data_tick_flea_7 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='tick_flea_7')
        data_heartworm_8 = VaccineUsed.objects.filter(vaccine_record=vaccine_record).get(disease='heartworm_8')


    if request.method == 'POST':
        # if is changed to TRUE, it cannot be changed back to FALSE 
        if vaccine_record.deworming_1 == True:
            vaccine_record.deworming_1 = vaccine_record.deworming_1
        else:
            vaccine_record.deworming_1 = bool(request.POST.get('deworming_1'))
        if vaccine_record.deworming_2 == True:
            vaccine_record.deworming_2 = vaccine_record.deworming_2
        else:
            vaccine_record.deworming_2 = bool(request.POST.get('deworming_2'))
        if vaccine_record.deworming_3 == True:
            vaccine_record.deworming_3 = vaccine_record.deworming_3
        else:
            vaccine_record.deworming_3 = bool(request.POST.get('deworming_3'))
        if vaccine_record.dhppil_cv_1 == True:
            vaccine_record.dhppil_cv_1 = vaccine_record.dhppil_cv_1
        else:
            vaccine_record.dhppil_cv_1 = bool(request.POST.get('dhppil_cv_1'))
        if vaccine_record.heartworm_1 == True:
            vaccine_record.heartworm_1 = vaccine_record.heartworm_1
        else:
            vaccine_record.heartworm_1 = bool(request.POST.get('heartworm_1'))
        if vaccine_record.bordetella_1 == True:
            vaccine_record.bordetella_1 = vaccine_record.bordetella_1
        else:
            vaccine_record.bordetella_1 = bool(request.POST.get('bordetella_1'))
        if vaccine_record.tick_flea_1 == True:
            vaccine_record.tick_flea_1 = vaccine_record.tick_flea_1
        else:
            vaccine_record.tick_flea_1 = bool(request.POST.get('tick_flea_1'))
        if vaccine_record.dhppil_cv_2 == True:
            vaccine_record.dhppil_cv_2 = vaccine_record.dhppil_cv_2
        else:
            vaccine_record.dhppil_cv_2 = bool(request.POST.get('dhppil_cv_2'))
        if vaccine_record.deworming_4 == True:
            vaccine_record.deworming_4 = vaccine_record.deworming_4
        else:
            vaccine_record.deworming_4 = bool(request.POST.get('deworming_4'))
        if vaccine_record.heartworm_2 == True:
            vaccine_record.heartworm_2 = vaccine_record.heartworm_2
        else:
            vaccine_record.heartworm_2 = bool(request.POST.get('heartworm_2'))
        if vaccine_record.bordetella_2 == True:
            vaccine_record.bordetella_2 = vaccine_record.bordetella_2
        else:
            vaccine_record.bordetella_2 = bool(request.POST.get('bordetella_2'))
        if vaccine_record.anti_rabies == True:
            vaccine_record.anti_rabies = vaccine_record.anti_rabies
        else:
            vaccine_record.anti_rabies = bool(request.POST.get('anti_rabies'))
        if vaccine_record.tick_flea_2 == True:
            vaccine_record.tick_flea_2 = vaccine_record.tick_flea_2
        else:
            vaccine_record.tick_flea_2 = bool(request.POST.get('tick_flea_2'))
        if vaccine_record.dhppil_cv_3 == True:
            vaccine_record.dhppil_cv_3 = vaccine_record.dhppil_cv_3
        else:
            vaccine_record.dhppil_cv_3 = bool(request.POST.get('dhppil_cv_3'))
        if vaccine_record.heartworm_3 == True:
            vaccine_record.heartworm_3 = vaccine_record.heartworm_3
        else:
            vaccine_record.heartworm_3 = bool(request.POST.get('heartworm_3'))
        if vaccine_record.dhppil4_1 == True:
            vaccine_record.dhppil4_1 = vaccine_record.dhppil4_1
        else:
            vaccine_record.dhppil4_1 = bool(request.POST.get('dhppil4_1'))
        if vaccine_record.tick_flea_3 == True:
            vaccine_record.tick_flea_3 = vaccine_record.tick_flea_3
        else:
            vaccine_record.tick_flea_3 = bool(request.POST.get('tick_flea_3'))
        if vaccine_record.dhppil4_2 == True:
            vaccine_record.dhppil4_2 = vaccine_record.dhppil4_2
        else:
            vaccine_record.dhppil4_2 = bool(request.POST.get('dhppil4_2'))
        if vaccine_record.heartworm_4 == True:
            vaccine_record.heartworm_4 = vaccine_record.heartworm_4
        else:
            vaccine_record.heartworm_4 = bool(request.POST.get('heartworm_4'))
        if vaccine_record.tick_flea_4 == True:
            vaccine_record.tick_flea_4 = vaccine_record.tick_flea_4
        else:
            vaccine_record.tick_flea_4 = bool(request.POST.get('tick_flea_4'))
        if vaccine_record.heartworm_5 == True:
            vaccine_record.heartworm_5 = vaccine_record.heartworm_5
        else:
            vaccine_record.heartworm_5 = bool(request.POST.get('heartworm_5'))
        if vaccine_record.tick_flea_5 == True:
            vaccine_record.tick_flea_5 = vaccine_record.tick_flea_5
        else:
            vaccine_record.tick_flea_5 = bool(request.POST.get('tick_flea_5'))
        if vaccine_record.heartworm_6 == True:
            vaccine_record.heartworm_6 = vaccine_record.heartworm_6
        else:
            vaccine_record.heartworm_6 = bool(request.POST.get('heartworm_6'))
        if vaccine_record.tick_flea_6 == True:
            vaccine_record.tick_flea_6 = vaccine_record.tick_flea_6
        else:
            vaccine_record.tick_flea_6 = bool(request.POST.get('tick_flea_6'))
        if vaccine_record.heartworm_7 == True:
            vaccine_record.heartworm_7 = vaccine_record.heartworm_7
        else:
            vaccine_record.heartworm_7 = bool(request.POST.get('heartworm_7'))
        if vaccine_record.tick_flea_7 == True:
            vaccine_record.tick_flea_7 = vaccine_record.tick_flea_7
        else:
            vaccine_record.tick_flea_7 = bool(request.POST.get('tick_flea_7'))
        if vaccine_record.heartworm_8 == True:
            vaccine_record.heartworm_8 = vaccine_record.heartworm_8
        else:
            vaccine_record.heartworm_8 = bool(request.POST.get('heartworm_8'))
        
       
        # ERASE ELSE when everything is WORKING
        if vaccine_record.deworming_1 == True and request.POST.get('s_deworming_1') !='' and request.POST.get('s_deworming_1') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_deworming_1'))
            med = Medicine_Inventory.objects.get(medicine=m)

            if med.quantity > 0:
                data_deworming_1.vaccine = m
                data_deworming_1.date_vaccinated = dtoday
                data_deworming_1.veterinary = current_user
                data_deworming_1.save()
                vaccine_record.save(update_fields=["deworming_1"]) 
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.deworming_2 == True and request.POST.get('s_deworming_2') !='' and request.POST.get('s_deworming_2') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_deworming_2'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_deworming_2.vaccine = m
                data_deworming_2.date_vaccinated = dtoday
                data_deworming_2.veterinary = current_user
                data_deworming_2.save()
                vaccine_record.save(update_fields=["deworming_2"]) 
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())
       
        if vaccine_record.deworming_3 == True and request.POST.get('s_deworming_3') !='' and request.POST.get('s_deworming_3') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_deworming_3'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_deworming_3.vaccine = m
                data_deworming_3.date_vaccinated = dtoday
                data_deworming_3.veterinary = current_user
                data_deworming_3.save()
                vaccine_record.save(update_fields=["deworming_3"]) 
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.dhppil_cv_1 == True and request.POST.get('s_dhppil_cv_1') != '' and request.POST.get('s_dhppil_cv_1') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_dhppil_cv_1'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_dhppil_cv_1.vaccine = m
                data_dhppil_cv_1.date_vaccinated = dtoday
                data_dhppil_cv_1.veterinary = current_user
                data_dhppil_cv_1.save()
                vaccine_record.save(update_fields=["dhppil_cv_1"]) 
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.heartworm_1 == True and request.POST.get('s_heartworm_1') !='' and request.POST.get('s_heartworm_1') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_heartworm_1'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_heartworm_1.vaccine = m
                data_heartworm_1.date_vaccinated = dtoday
                data_heartworm_1.veterinary = current_user
                data_heartworm_1.save()
                vaccine_record.save(update_fields=["heartworm_1"]) 
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.bordetella_1 == True and request.POST.get('s_bordetella_1') !='' and request.POST.get('s_bordetella_1') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_bordetella_1'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_bordetella_1.vaccine = m
                data_bordetella_1.date_vaccinated = dtoday
                data_bordetella_1.veterinary = current_user
                data_bordetella_1.save()
                vaccine_record.save(update_fields=["bordetella_1"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.tick_flea_1 == True and request.POST.get('s_tick_flea_1') !='' and request.POST.get('s_tick_flea_1') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_tick_flea_1'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_tick_flea_1.vaccine = m
                data_tick_flea_1.date_vaccinated = dtoday
                data_tick_flea_1.veterinary = current_user
                data_tick_flea_1.save()
                vaccine_record.save(update_fields=["tick_flea_1"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.dhppil_cv_2 == True and request.POST.get('s_dhppil_cv_2') !='' and request.POST.get('s_dhppil_cv_2') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_dhppil_cv_2'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_dhppil_cv_2.vaccine = m
                data_dhppil_cv_2.date_vaccinated = dtoday
                data_dhppil_cv_2.veterinary = current_user
                data_dhppil_cv_2.save()
                vaccine_record.save(update_fields=["dhppil_cv_2"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())
            
        if vaccine_record.deworming_4 == True and request.POST.get('s_deworming_4') !='' and request.POST.get('s_deworming_4') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_deworming_4'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_deworming_4.vaccine = m
                data_deworming_4.date_vaccinated = dtoday
                data_deworming_4.veterinary = current_user
                data_deworming_4.save()
                vaccine_record.save(update_fields=["deworming_4"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.heartworm_2 == True and request.POST.get('s_heartworm_2') !='' and request.POST.get('s_heartworm_2') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_heartworm_2'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_heartworm_2.vaccine = m
                data_heartworm_2.date_vaccinated = dtoday
                data_heartworm_2.veterinary = current_user
                data_heartworm_2.save()
                vaccine_record.save(update_fields=["heartworm_2"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.bordetella_2 == True and request.POST.get('s_bordetella_2') !='' and request.POST.get('s_bordetella_2') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_bordetella_2'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_bordetella_2.vaccine = m
                data_bordetella_2.date_vaccinated = dtoday
                data_bordetella_2.veterinary = current_user
                data_bordetella_2.save()
                vaccine_record.save(update_fields=["bordetella_2"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.anti_rabies == True and request.POST.get('s_anti_rabies') !='' and request.POST.get('s_anti_rabies') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_anti_rabies'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_anti_rabies.vaccine = m
                data_anti_rabies.date_vaccinated = dtoday
                data_anti_rabies.veterinary = current_user
                data_anti_rabies.save()
                vaccine_record.save(update_fields=["anti_rabies"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.tick_flea_2 == True and request.POST.get('s_tick_flea_2') !='' and request.POST.get('s_tick_flea_2') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_tick_flea_2'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_tick_flea_2.vaccine = m
                data_tick_flea_2.date_vaccinated = dtoday
                data_tick_flea_2.veterinary = current_user
                data_tick_flea_2.save()
                vaccine_record.save(update_fields=["anti_rabies"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.dhppil_cv_3 == True and request.POST.get('s_dhppil_cv_3') !='' and request.POST.get('s_dhppil_cv_3') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_dhppil_cv_3'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_dhppil_cv_3.vaccine = m
                data_dhppil_cv_3.date_vaccinated = dtoday
                data_dhppil_cv_3.veterinary = current_user
                data_dhppil_cv_3.save()
                vaccine_record.save(update_fields=["dhppil_cv_3"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.heartworm_3 == True and request.POST.get('s_heartworm_3') !='' and request.POST.get('s_heartworm_3') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_heartworm_3'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_heartworm_3.vaccine = m
                data_heartworm_3.date_vaccinated = dtoday
                data_heartworm_3.veterinary = current_user
                data_heartworm_3.save()
                vaccine_record.save(update_fields=["dhppil_cv_3"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.dhppil4_1 == True and request.POST.get('s_dhppil4_1') !='' and request.POST.get('s_dhppil4_1') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_dhppil4_1'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_dhppil4_1.vaccine = m
                data_dhppil4_1.date_vaccinated = dtoday
                data_dhppil4_1.veterinary = current_user
                data_dhppil4_1.save()
                vaccine_record.save(update_fields=["dhppil4_1"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.tick_flea_3 == True and request.POST.get('s_tick_flea_3') !='' and request.POST.get('s_tick_flea_3') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_tick_flea_3'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_tick_flea_3.vaccine = m
                data_tick_flea_3.date_vaccinated = dtoday
                data_tick_flea_3.veterinary = current_user
                data_tick_flea_3.save()
                vaccine_record.save(update_fields=["tick_flea_3"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.dhppil4_2 == True and request.POST.get('s_dhppil4_2') !='' and request.POST.get('s_dhppil4_2') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_dhppil4_2'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_dhppil4_2.vaccine = m
                data_dhppil4_2.date_vaccinated = dtoday
                data_dhppil4_2.veterinary = current_user
                data_dhppil4_2.save()
                vaccine_record.save(update_fields=["dhppil4_2"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.heartworm_4 == True and request.POST.get('s_heartworm_4') !='' and request.POST.get('s_heartworm_4') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_heartworm_4'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_heartworm_4.vaccine = m
                data_heartworm_4.date_vaccinated = dtoday
                data_heartworm_4.veterinary = current_user
                data_heartworm_4.save()
                vaccine_record.save(update_fields=["heartworm_4"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.tick_flea_4 == True and request.POST.get('s_tick_flea_4') !='' and request.POST.get('s_tick_flea_4') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_tick_flea_4'))
            if med.quantity > 0:
                med = Medicine_Inventory.objects.get(medicine=m)
                data_tick_flea_4.vaccine = m
                data_tick_flea_4.date_vaccinated = dtoday
                data_tick_flea_4.veterinary = current_user
                data_tick_flea_4.save()
                vaccine_record.save(update_fields=["tick_flea_4"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.heartworm_5 == True and request.POST.get('s_heartworm_5') !='' and request.POST.get('s_heartworm_5') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_heartworm_5'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_heartworm_5.vaccine = m
                data_heartworm_5.date_vaccinated = dtoday
                data_heartworm_5.veterinary = current_user
                data_heartworm_5.save()
                vaccine_record.save(update_fields=["heartworm_5"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.tick_flea_5 == True and request.POST.get('s_tick_flea_5') !='' and request.POST.get('s_tick_flea_5') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_tick_flea_5'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_tick_flea_5.vaccine = m
                data_tick_flea_5.date_vaccinated = dtoday
                data_tick_flea_5.veterinary = current_user
                data_tick_flea_5.save()
                vaccine_record.save(update_fields=["tick_flea_5"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.heartworm_6 == True and request.POST.get('s_heartworm_6') !='' and request.POST.get('s_heartworm_6') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_heartworm_6'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_heartworm_6.vaccine = m
                data_heartworm_6.date_vaccinated = dtoday
                data_heartworm_6.veterinary = current_user
                data_heartworm_6.save()
                vaccine_record.save(update_fields=["heartworm_6"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.tick_flea_6 == True and request.POST.get('s_tick_flea_6') !='' and request.POST.get('s_tick_flea_6') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_tick_flea_6'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_tick_flea_6.vaccine = m
                data_tick_flea_6.date_vaccinated = dtoday
                data_tick_flea_6.veterinary = current_user
                data_tick_flea_6.save()
                vaccine_record.save(update_fields=["tick_flea_6"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.heartworm_7 == True and request.POST.get('s_heartworm_7') !='' and request.POST.get('s_heartworm_7') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_heartworm_7'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_heartworm_7.vaccine = m
                data_heartworm_7.date_vaccinated = dtoday
                data_heartworm_7.veterinary = current_user
                data_heartworm_7.save()
                vaccine_record.save(update_fields=["heartworm_7"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.tick_flea_7 == True and request.POST.get('s_tick_flea_7') !='' and request.POST.get('s_tick_flea_7') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_tick_flea_7'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_tick_flea_7.vaccine = m
                data_tick_flea_7.date_vaccinated = dtoday
                data_tick_flea_7.veterinary = current_user
                data_tick_flea_7.save()
                vaccine_record.save(update_fields=["tick_flea_7"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        if vaccine_record.heartworm_8 == True and request.POST.get('s_heartworm_8') !='' and request.POST.get('s_heartworm_8') !=None:
            m = Medicine.objects.get(medicine=request.POST.get('s_heartworm_8'))
            med = Medicine_Inventory.objects.get(medicine=m)
            if med.quantity > 0:
                data_heartworm_8.vaccine = m
                data_heartworm_8.date_vaccinated = dtoday
                data_heartworm_8.veterinary = current_user
                data_heartworm_8.save()
                vaccine_record.save(update_fields=["heartworm_8"])
                med.quantity = med.quantity - 1
                med.save()
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = 1, date_subtracted = dtoday, time = dt.datetime.now())

        messages.success(request, 'Preventive Health Program Updated!')
        return redirect('unitmanagement:health_history', id = id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'dog_days': dog_days,
        'style': style,
        'title': "Health History of ",
        'name': data.name,
        'actiontype': "Submit",
        'data': data,
        'health_data': health_data,
        'phyexam_data': phyexam_data,
        'vaccine_record': vaccine_record,
        'dtoday':dtoday,
        'form1': vaccine_record_form,
        'form2': vaccine_used_form,
        'vaccine_available':vaccine_available,
        'active_1':active_1,
        'active_2':active_2,
        'active_3':active_3,
        'data_deworming_1':data_deworming_1,
        'data_deworming_2':data_deworming_2,
        'data_deworming_3':data_deworming_3,
        'data_dhppil_cv_1':data_dhppil_cv_1,
        'data_heartworm_1':data_heartworm_1,
        'data_bordetella_1':data_bordetella_1,
        'data_tick_flea_1':data_tick_flea_1,
        'data_dhppil_cv_2':data_dhppil_cv_2,
        'data_deworming_4':data_deworming_4,
        'data_heartworm_2':data_heartworm_2,
        'data_bordetella_2':data_bordetella_2,
        'data_anti_rabies':data_anti_rabies,
        'data_tick_flea_2':data_tick_flea_2,
        'data_dhppil_cv_3':data_dhppil_cv_3,
        'data_heartworm_3':data_heartworm_3,
        'data_dhppil4_1':data_dhppil4_1,
        'data_tick_flea_3':data_tick_flea_3,
        'data_dhppil4_2':data_dhppil4_2,
        'data_heartworm_4':data_heartworm_4,
        'data_tick_flea_4':data_tick_flea_4,
        'data_heartworm_5':data_heartworm_5,
        'data_tick_flea_5':data_tick_flea_5,
        'data_heartworm_6':data_heartworm_6,
        'data_tick_flea_6':data_tick_flea_6,
        'data_heartworm_7':data_heartworm_7,
        'data_tick_flea_7':data_tick_flea_7,
        'data_heartworm_8':data_heartworm_8,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/health_history.html', context)

def health_details(request, id):
    data = Health.objects.get(id=id)
    i = K9_Incident.objects.get(id=data.incident_id.id)
    medicine = HealthMedicine.objects.filter(health=data)
    dog = K9.objects.get(id = data.dog.id)
   
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Prescription of ",
        'name': dog.name,
        'date': data.date,
        'data': data,
        'medicine': medicine,
        'dog': dog,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/health_details.html', context)

def physical_exam_details(request, id):
    data = PhysicalExam.objects.get(id=id)
    dog = K9.objects.get(id = data.dog.id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Physical Exam Details of",
        'name': dog.name,
        'data': data,
        'dog': dog,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/physical_exam_details.html', context)

#Approval of medicine
def medicine_approve(request, id):
    data = Health.objects.get(id=id) #get health details
    medicine = HealthMedicine.objects.filter(health=data) #get medicine in health
    count = 0

    for med in medicine: #form items
        i = Medicine_Inventory.objects.filter(id = med.medicine.id) # get Inventory Items
        for x in i:
            print("Inventory Items", x.medicine, x.quantity)
            print("Form Items", med.medicine, med.quantity)
            if (x.quantity >= med.quantity):
                count = count+1

    print(count)
    user_serial = request.session['session_serial']
    user = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user.UserID.id)

    if medicine.count() == count:
        for med in medicine:
            i = Medicine_Inventory.objects.filter(id = med.medicine.id) # get Inventory Items
            for x in i:
                Medicine_Subtracted_Trail.objects.create(inventory = x, user = current_user, quantity = med.quantity, date_subtracted = dt.date.today(), time = dt.datetime.now())
                x.quantity = (x.quantity - med.quantity)
                data.status = "Approved"
                data.save()
                x.save()

        messages.success(request, 'Medicine Acquisition has been approved!')
    else:
        messages.warning(request, 'Insufficient Inventory!')
        return redirect('unitmanagement:health_details', id = data.id)

    return redirect('unitmanagement:health_details', id = data.id)

# Vaccination form
def vaccination_form(request):
    form = VaccinationUsedForm(request.POST or None)
    style=""
    if request.method == 'POST':
        if form.is_valid():
            v = request.POST.get('vaccine')
            med = Medicine_Inventory.objects.get(medicine=v)
            if med.quantity != 0:
                form.save()
                new_form = form.save()
                #get vaccine yearly-Used
                vaccine = Medicine.objects.get(id=new_form.vaccine.id)
                duration = 365 / vaccine.used_yearly
                new_form.date_validity = dt.date.today() + dt.timedelta(days=duration)
                new_form.save()

                user_serial = request.session['session_serial']
                user = Account.objects.get(serial_number=user_serial)
                current_user = User.objects.get(id=user.UserID.id)

                q = med.quantity-1
                Medicine_Subtracted_Trail.objects.create(inventory = med, user = current_user, quantity = q, date_subtracted = dt.date.today(), time = dt.datetime.now())
                style = "ui green message"
                messages.success(request, 'Vaccination has been successfully recorded!')
                form = VaccinationUsedForm()
            else:
                style = "ui red message"
                messages.warning(request, 'Insufficient Inventory Quantity!')
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Vaccination",
        'actiontype': "Submit",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/vaccination_form.html', context)

def requests_form(request):
    style=""

    form = RequestForm(request.POST or None)
    
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            
            no_id = form.save()
            no_id.handler =user_session(request)
            no_id.save()

            style = "ui green message"
            messages.success(request, 'Request has been successfully recorded!')
            form = RequestForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Request of equipment",
        'actiontype': "Submit",
        'style': style,
        'form': form,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/request_form.html', context)

def request_list(request):
    data = Requests.objects.all()

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'data': data,
        'title': 'Damaged Equipment List',
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/request_list.html', context)

def change_equipment(request, id):
    data = Requests.objects.get(id=id)
    style = ""
    changedate = dt.datetime.now()

    if request.method == 'POST':
        if 'ok' in request.POST:
            data.request_status = "Approved"
            data.date_approved = changedate
            data.save()
            #subtract inventory
            equipment = Miscellaneous.objects.get(miscellaneous=data.equipment)
            if equipment.quantity > 0:
                equipment.quantity = equipment.quantity-1
                equipment.save()

                Miscellaneous_Subtracted_Trail.objects.create(inventory=equipment, user=user_session(request),
                                                         quantity=1,
                                                         date_subtracted=dt.date.today(),
                                                         time=dt.datetime.now())
                style = "ui green message"
                messages.success(request, 'Equipment Approved!')

            else:
                style = "ui red message"
                messages.success(request, 'Insufficient Inventory!')

        else:
            data.request_status = "Denied"
            data.date_approved = changedate
            data.save()
            style = "ui green message"
            messages.success(request, 'Equipment Denied!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'data': data,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render (request, 'unitmanagement/change_equipment.html', context)

# TODO
def k9_incident(request):
    form = K9IncidentForm(request.POST or None)
    style=''
    
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)

    if request.method == "POST":
        if form.is_valid():
            incident_save = form.save()
            incident_save.reported_by = str(user_in_session.fullname)
            incident_save.save()
            
            # get k9 object
            k9 =incident_save.k9
            k9_obj=K9.objects.get(id=k9.id)

            #if k9 has a partner handler and died
            if k9_obj.partnered==True and incident_save.incident=='Died' :
                handler = User.objects.get(id=k9_obj.handler.id)
                k9_obj.status = 'Dead'
                k9_obj.handler = None
                k9_obj.partnered= False
                handler.partnered = False
                k9_obj.save()
                handler.save()
            elif k9_obj.partnered==False and incident_save.incident=='Died' :
                k9_obj.status = 'Dead'
                k9_obj.save()
            elif incident_save.incident=='Sick' :
                k9_obj.status = 'Sick'
                k9_obj.save()

            form = K9IncidentForm()
            style = "ui green message"
            messages.success(request, 'Incident has been successfully Reported!')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "K9 Incident",
        'actiontype': "Submit",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/k9_incident.html', context)

def handler_incident(request):
    form = HandlerIncidentForm(request.POST or None)
    style=''
    user_serial = request.session['session_serial']
    user_s = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user_s.UserID.id)

    if current_user.position == 'Handler':
        form.initial['handler'] = current_user
    if request.method == "POST":
        if form.is_valid():
            incident_save = form.save()
            incident_save.status='Done'
            incident_save.save()
            # get k9 object
            handler =incident_save.handler
            handler_obj=User.objects.get(id=handler.id)
            
            #if k9 has a partner handler and died
            if handler_obj.partnered==True and incident_save.incident=='Died' :
                k9 = K9.objects.get(handler_id=handler_obj.id)
                handler_obj.partnered = False
                handler_obj.status = 'Dead'
                k9.partnered = False
                k9.handler = None
                print(k9, k9.handler)
                k9.save()
                handler_obj.save()
            else:
                handler_obj.status = 'Dead'
                handler_obj.save()

            form = HandlerIncidentForm()
            style = "ui green message"
            messages.success(request, 'Incident has been successfully Reported!')
        
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Handler Incident",
        'actiontype': "Submit",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/handler_incident.html', context)

def on_leave_request(request):
    form = HandlerOnLeaveForm(request.POST or None)
    style=''
  
    form.initial['handler'] = user_session(request)
    if request.method == "POST":
        if form.is_valid():
            incident_save = form.save()
            
            form = HandlerOnLeaveForm()
            style = "ui green message"
            messages.success(request, 'Request has been successfully Submited!')
        
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "On-Leave Form",
        'actiontype': "Submit",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/on_leave_form.html', context)

def reassign_assets(request):
    style=''
    form = ReassignAssetsForm(request.POST or None)
    k9 = K9.objects.filter(training_status='For-Deployment').filter(partnered=False)
    handler = User.objects.filter(status='Working').filter(position='Handler').filter(partnered=False)
    numh = handler.count()
    numk = k9.count()
    if request.method == 'POST':
        print('yes')
        if form.is_valid():
            k9 = K9.objects.get(id=form.data['k9'])
            handler = User.objects.get(id=form.data['handler'])

            #save status
            k9.handler = handler
            k9.partnered = True
            k9.save()

            handler.partnered = True
            handler.save()

            form = ReassignAssetsForm()
            style = "ui green message"
            messages.success(request, 'Assets has been successfully Partnered!')
        else:
            style = "ui red message"
            messages.warning(request, 'Make sure all input is complete!')
        
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Reassign Assets",
        'actiontype': "Submit",
        'style': style,
        'form': form,
        'handler': handler,
        'k9':k9,
        'numk': numk,
        'numh': numh,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/reassign_assets.html', context)

# TODO 
# On Leave List
def on_leave_list(request):
    style=''
    data1 = Handler_Incident.objects.filter(status='Pending').filter(incident='On-Leave') 
    data2 = Handler_Incident.objects.filter(status='Approved').filter(incident='On-Leave') 
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "On Leave Request List",
        'data1': data1,
        'data2': data2,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/on_leave_list.html', context)

#TODO
# what to do if on-leave
def on_leave_details(request, id):
    style=''
    data = Handler_Incident.objects.get(id=id)
    #get k9 
    days = data.date_to - data.date_from
    #get user
    u = User.objects.get(id=data.handler.id)
    try:
        k9 = K9.objects.get(handler=data.handler)
        data.k9 = k9
        data.save()
    except K9.DoesNotExist:
        k9 = None

    if request.method == 'POST':
        #get checkbox
        c = request.POST.get("return_k9")
        if 'approve' in request.POST:
            data.status = "Approved"
            data.save()
            if c == None:
                k9.handler_on_leave = False
                k9.save()
            elif c == 'on':
                k9.handler_on_leave = True
                k9.save()
            # change status of handler to On leave
            u.status = 'On-Leave'
            u.partnered = False
            u.save()
            # What to do with k9?
            k9.training_status = 'For-Deployment'
            k9.assignment = None
            k9.partnered = False
            k9.save()

            # If deployed, pull out
            try:
                td = Team_Dog_Deployed.objects.filter(k9=k9).filter(status='Deployed').latest()
                td.status = 'Done'
                td.date_pulled = date.today()
                td.save()

                try:
                    ta = Team_Assignment.objects.get(id=td.team_assignment.id)
                    if k9.capability == 'EDD':
                        ta.EDD_deployed = ta.EDD_deployed-1
                    elif k9.capability == 'NDD':
                        ta.NDD_deployed = ta.NDD_deployed-1
                    elif k9.capability == 'SAR':
                        ta.SAR_deployed = ta.SAR_deployed-1

                    ta.save()
                except Team_Assignment.DoesNotExist:
                    pass
            except Team_Dog_Deployed.DoesNotExist:
                pass

            #Make Notification
            return HttpResponseRedirect('../on-leave-list/')
        elif 'deny' in request.POST:
            data.status = "Denied"
            data.save()
            #Make Notification
            return HttpResponseRedirect('../on-leave-list/')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': str(data.handler) + ' On-Leave Request',
        'data': data,
        'k9': k9,
        'days': days,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/on_leave_details.html', context)

#TODO reassign
def load_hander(request):
    k9 = request.GET.get('k9')
    handler = User.objects.filter(position=Handler).filter(status='Working').filter(capability=k9.capability).order_by('name')
    return render(request, 'unitmanagement/handler_dropdown.html', {'handler': handler})

# TODO 
# Reproductive Cycle
def reproductive_list(request):
    style=''
    proestrus = K9.objects.filter(reproductive_stage='Proestrus').filter(sex='Female')
    estrus = K9.objects.filter(reproductive_stage='Estrus').filter(sex='Female')
    metestrus = K9.objects.filter(reproductive_stage='Metestrus').filter(sex='Female')
    anestrus = K9.objects.filter(reproductive_stage='Anestrus').filter(sex='Female')
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Reproductive Cycle",
        'proestrus': proestrus,
        'estrus': estrus,
        'metestrus': metestrus,
        'anestrus': anestrus,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/reproductive_list.html', context)

def reproductive_edit(request, id):
    style=''
    data = K9.objects.get(id=id)
    form = ReproductiveForm(request.POST or None, instance = data)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Reproductive Details has been successfully Updated!')
        else:
            style = "ui red message"
            messages.warning(request, 'Make sure all input is complete!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Reproductive Details",
        'data': data,
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/reproductive_details.html', context)

# TODO 
# k9_unpartnered_list Cycle
def k9_unpartnered_list(request):
    style=''
    data = K9.objects.filter(handler_on_leave=False).filter(training_status='For-Deployment').filter(partnered=False)
    data2 = K9.objects.filter(handler_on_leave=True).filter(training_status='For-Deployment').filter(partnered=False)
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Unpartnered K9 List",
        'data':data,
        'data2':data2,
        'style':style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/k9_unpartnered_list.html', context)

# TODO 
# choose_handler Cycle
def choose_handler_list(request, id):
    style=''
    k9 = K9.objects.get(id=id)
    data = User.objects.filter(status='Working').filter(position='Handler').filter(capability=k9.capability).filter(partnered=False)
    data_available = User.objects.filter(status='Working').filter(position='Handler').filter(partnered=False).exclude(capability=k9.capability)
    print(data_available)
    data_pi = Personal_Info.objects.filter(UserID__in=data)
    data_pi2 = Personal_Info.objects.filter(UserID__in=data_available)

    request.session["k9_id_partnered"] = k9.id 
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': k9,
        'data':data,
        'k9':k9,
        'style':style,
        'data_pi': data_pi,
        'data_pi2':data_pi2,
        'data_available': data_available,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/choose_handler_list.html', context)

# TODO 
# choose_handler Cycle
def choose_handler(request, id):
    k9_id_partnered = request.session["k9_id_partnered"]
    k9 = K9.objects.get(id=k9_id_partnered)
    handler = User.objects.get(id=id)

    k9.handler = handler
    k9.partnered = True
    k9.save()

    handler.partnered = True
    handler.capability = k9.capability
    handler.save()

    messages.success(request, 'Assets has been successfully Partnered!')
     
    return redirect('unitmanagement:k9_unpartnered_list')

#TODO
#sick list
def k9_sick_list(request):
    
    data = K9_Incident.objects.filter(incident='Sick').filter(status='Pending')
    data2 = K9_Incident.objects.filter(incident='Sick').filter(status='Done')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    style = "ui green message"
    context = {
        'title': 'Sick K9s',
        'data':data,
        'data2':data2,
        'notif_data':notif_data,
        'count':count,
        'style':style,
        'user':user,
    }
    return render (request, 'unitmanagement/k9_sick_list.html', context)

#TODO
#sick list
def k9_sick_details(request, id):
    
    data = K9_Incident.objects.get(id=id)

    medicine_formset = inlineformset_factory(Health, HealthMedicine, form=HealthMedicineForm, extra=1, can_delete=True)
    style=""

    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)

    form = HealthForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            #get treatment
            request.session['treatment'] = form['treatment'].value()

            m = form.save()
            m.dog = data.k9
            m.problem  = data.description
            m.incident_id = data
            m.veterinary = user_in_session
            m.save()
            new_form = m.pk
            form_instance = Health.objects.get(id=new_form)
            dog = K9.objects.get(id=form_instance.dog.id)
            
            #Use Health form instance for Health Medicine
            formset = medicine_formset(request.POST, instance=form_instance)
            form_med = []
            form_quantity = []
            inventory_quantity = []
            insufficient_quantity = []
            insufficient_med = []
            days = []
            
            msg = 'Insuficient quantity! Availability for '

            if formset.is_valid():
                for form in formset:
                    m = Medicine.objects.get(medicine_fullname= form.cleaned_data['medicine'])
                    form_med.append(m)
                    form_quantity.append(form.cleaned_data['quantity'])
                    days.append(form.cleaned_data['duration'])

                mi = Medicine_Inventory.objects.filter(medicine__in=form_med)
                
                for mi in mi:
                    inventory_quantity.append(mi.quantity)

                ctr1 = 0
                ctr2 = len(form_quantity)
              
                while ctr1 < ctr2:
                    if inventory_quantity[ctr1] >= form_quantity[ctr1]:
                        pass
                    else:
                        insufficient_quantity.append(inventory_quantity[ctr1])
                        insufficient_med.append(form_med[ctr1])
                    ctr1=ctr1+1

                ctr3 = len(insufficient_med)
                ctr4=0

                if ctr3 != 0:
                    while ctr4 < ctr3:
                        if ctr4 == ctr3-1:
                            msg = msg + str(insufficient_med[ctr4]) + ': ' + str(insufficient_quantity[ctr4]) + 'pcs.'
                        else:
                            msg = msg + str(insufficient_med[ctr4]) + ': ' + str(insufficient_quantity[ctr4]) + 'pcs, '
                        ctr4=ctr4+1
                    form_instance.delete()
                    style = "ui red message"
                    messages.warning(request, msg)        
                else:
                    m.duration =  max(days)
                    m.save()

                    for form in formset:
                        f = form.save()
                        m = Medicine_Inventory.objects.get(id=f.medicine.id)
                        m.quantity = m.quantity - f.quantity
                        m.save()
                        #Medicine_Subtracted_Trail.objects.create(inventory = m, user=current_user(), quantity = f.quantity)
                    dog.status = 'Sick'
                    data.status= 'Done'
                    dog.save()
                    data.save()
                    style = "ui green message"
                    messages.success(request, 'Health Form has been successfully recorded!')
                    return redirect('unitmanagement:k9_sick_list')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': data.k9,
        'data':data,
        'form':HealthForm,
        'formset':medicine_formset(),
        'actiontype': "Submit",
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/k9_sick_details.html', context)

#TODO
class K9ListView(APIView):
    def get(self, request):
        data = K9.objects.filter(partnered=False).exclude(status='Dead').filter(training_status='For-Deployment')
        serializer = K9Serializer(data, many=True)
        return Response(serializer.data)

    def put(self, request):
        serializer = K9Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def save(self, *args, **kwargs):
        super(K9, self).save()

class K9DetailView(APIView):
    def get(self, request, id):
        notif = get_object_or_404(K9, id=id)
        serializer = K9Serializer(notif)
        return Response(serializer.data)

    def delete(self, request, id):
        notif = get_object_or_404(K9, id=id)
        notif.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#TODO
class UserListView(APIView):
    def get(self, request):
        data = User.objects.filter(partnered=False).filter(position='Handler').filter(status='Working')
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get(self, request, id):
        notif = get_object_or_404(User, id=id)
        serializer = UserSerializer(notif)
        return Response(serializer.data)

    def delete(self, request, id):
        notif = get_object_or_404(User, id=id)
        notif.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)