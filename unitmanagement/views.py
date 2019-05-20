from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.db.models import aggregates
from django.contrib import messages
import datetime as dt
from datetime import timedelta, date
from decimal import Decimal
import itertools
from django.db.models import Sum, Avg, Max
from django.core.exceptions import ObjectDoesNotExist

from planningandacquiring.forms import k9_detail_form
from planningandacquiring.models import K9
from unitmanagement.models import PhysicalExam, Health, HealthMedicine, K9_Incident, Handler_On_Leave, K9_Incident, Handler_K9_History
from unitmanagement.forms import PhysicalExamForm, HealthForm, HealthMedicineForm, VaccinationRecordForm, RequestForm, HandlerOnLeaveForm
from unitmanagement.forms import K9IncidentForm, HandlerIncidentForm, VaccinationUsedForm, ReassignAssetsForm, ReproductiveForm
from inventory.models import Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Miscellaneous_Subtracted_Trail
from inventory.models import Medicine_Received_Trail, Food_Subtracted_Trail, Food
from unitmanagement.models import HealthMedicine, Health, VaccinceRecord, Equipment_Request, VaccineUsed, Notification, Image
from deployment.models import K9_Schedule, Dog_Request, Team_Dog_Deployed, Team_Assignment
from profiles.models import User, Account, Personal_Info
from training.models import K9_Handler
from training.forms import assign_handler_form

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
    elif notif.notif_type == 'retired_k9' :
        notif.viewed = True
        notif.save()
        return redirect('planningandacquiring:K9_detail', id = notif.k9.id)
    elif notif.notif_type == 'medicine_done' :
        notif.viewed = True
        notif.save()
        return redirect('unitmanagement:health_details', id = notif.other_id)
    #TODO location incident view details 
    # elif notif.notif_type == 'location_incident' :
    #     notif.viewed = True
    #     notif.save()
    #     return redirect('deployment:incident_detail', id = notif.other_id)
    

def index(request):
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    n = None
    try:
        n = Notification.objects.filter(user__id=id)
        print(n)
    except:
        pass

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'n':n,
    }        
    return render (request, 'unitmanagement/index.html', context)

#TODO Initialize treatment
def health_form(request):
    medicine_formset = inlineformset_factory(Health, HealthMedicine, form=HealthMedicineForm, extra=1, can_delete=True)
    style=""

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
        data = K9.objects.get(handler=handler)

    else:
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

    vr = VaccinceRecord.objects.get(k9=data)
    vu = VaccineUsed.objects.filter(vaccine_record=vr)
    style = 'ui green message'

    VaccinationUsedFormset= inlineformset_factory(VaccinceRecord, VaccineUsed, form=VaccinationUsedForm, extra=0)
    formset = VaccinationUsedFormset(request.POST or None, request.FILES or None, prefix='record', instance=vr)

    active_1 = ' active'
    active_2 = ''
    active_3 = ''

    ctr=0
    ctr1=0
    if request.method == 'POST':
        formset = VaccinationUsedFormset(request.POST, request.FILES, prefix='record', instance=vr)
        
        if formset.is_valid():
            for forms in formset:
                if forms.is_valid():
                    f = forms.save(commit=False)
                    if f.vaccine != None and f.date_vaccinated != None and f.done == False:  
                        ctr1=ctr1+1
                        f.veterinary = current_user
                        f.done = True
                        f.save()
                       
                        if f.disease == '1st Deworming':
                            vr.deworming_1 = True
                        elif f.disease == '2nd Deworming':
                            vr.deworming_2 = True
                        elif f.disease == '3rd Deworming':
                            vr.deworming_3 = True
                        elif f.disease == '1st dose DHPPiL+CV Vaccination':
                            vr.dhppil_cv_1 = True
                        elif f.disease == '1st Heartworm Prevention':
                            vr.heartworm_1 = True
                        elif f.disease == '1st dose Bordetella Bronchiseptica Bacterin':
                            vr.bordetella_1 = True
                        elif f.disease == '1st Tick and Flea Prevention':
                            vr.tick_flea_1 = True
                        elif f.disease == '2nd dose DHPPiL+CV Vaccination':
                            vr.dhppil_cv_2 = True
                        elif f.disease == '4th Deworming':
                            vr.deworming_4 = True
                        elif f.disease == '2nd Heartworm Prevention':
                            vr.heartworm_2 = True
                        elif f.disease == '2nd dose Bordetella Bronchiseptica Bacterin':
                            vr.bordetella_2 = True
                        elif f.disease == 'Anti-Rabies Vaccination	':
                            vr.anti_rabies = True
                        elif f.disease == '2nd Tick and Flea Prevention':
                            vr.tick_flea_2 = True
                        elif f.disease == '3rd dose DHPPiL+CV Vaccination':
                            vr.dhppil_cv_3 = True
                        elif f.disease == '3rd Heartworm Prevention':
                            vr.heartworm_3 = True
                        elif f.disease == '1st dose DHPPiL4 Vaccination':
                            vr.dhppil4_1 = True
                        elif f.disease == '3rd Tick and Flea Prevention':
                            vr.tick_flea_3 = True
                        elif f.disease == '2nd dose DHPPiL4 Vaccination':
                            vr.dhppil4_2 = True
                        elif f.disease == '4th Heartworm Prevention':
                            vr.heartworm_4 = True
                        elif f.disease == '4th Tick and Flea Prevention':
                            vr.tick_flea_4 = True
                        elif f.disease == '5th Heartworm Prevention':
                            vr.heartworm_5 = True
                        elif f.disease == '6th Heartworm Prevention':
                            vr.heartworm_6 = True
                        elif f.disease == '2nd dose DHPPiL4 Vaccination':
                            vr.bordetella_2 = True
                        elif f.disease == '6th Tick and Flea Prevention':
                            vr.tick_flea_6 = True
                        elif f.disease == '7th Heartworm Prevention':
                            vr.heartworm_7 = True
                        elif f.disease == '7th Tick and Flea Prevention':
                            vr.tick_flea_7 = True
                        elif f.disease == '8th Heartworm Prevention':
                            vr.heartworm_8 = True
                        vr.save()
                        
                        
                    else: 
                        pass
                    
                    if f.image != None:
                        ctr1=ctr1+1
                        f.save(update_fields=["image"])

                    if f.done == False and f.vaccine != None and f.date_vaccinated == None:
                        ctr = ctr+1
                    elif f.done == False and f.vaccine == None and f.date_vaccinated != None:
                        ctr = ctr+1

            print('ctr1: ',ctr1)
            print('ctr: ',ctr)
            if ctr1>27:
                messages.success(request, 'Prevention Updated!')
                return redirect('unitmanagement:health_history', id=data.id)

            if ctr>0:
                messages.success(request, 'Incomplete input. Please check again.')
                style='ui red message'

    for forms in formset:
        if forms.initial['disease'] == '1st Deworming' or forms.initial['disease'] == '2nd Deworming' or forms.initial['disease'] == '3rd Deworming' or forms.initial['disease'] == '4th Deworming':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Deworming').exclude(quantity=0)
           
        if forms.initial['disease'] == '1st dose DHPPiL+CV Vaccination' or forms.initial['disease'] == '2nd dose DHPPiL+CV Vaccination' or forms.initial['disease'] == '3rd dose DHPPiL+CV Vaccination':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='DHPPiL+CV').exclude(quantity=0)

        if forms.initial['disease'] == '1st Heartworm Prevention' or forms.initial['disease'] == '2nd Heartworm Prevention' or forms.initial['disease'] == '3rd Heartworm Prevention' or forms.initial['disease'] == '4th Heartworm Prevention' or forms.initial['disease'] == '5th Heartworm Prevention' or forms.initial['disease'] == '6th Heartworm Prevention' or forms.initial['disease'] == '7th Heartworm Prevention' or forms.initial['disease'] == '8th Heartworm Prevention':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Heartworm').exclude(quantity=0)

        if forms.initial['disease'] == 'Anti-Rabies Vaccination':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Anti-Rabies').exclude(quantity=0)
            
        if forms.initial['disease'] == '1st Tick and Flea Prevention' or forms.initial['disease'] == '2nd Tick and Flea Prevention' or forms.initial['disease'] == '3rd Tick and Flea Prevention' or forms.initial['disease'] == '4th Tick and Flea Prevention' or forms.initial['disease'] == '5th Tick and Flea Prevention' or forms.initial['disease'] == '6th Tick and Flea Prevention' or forms.initial['disease'] == '7th Tick and Flea Prevention':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Tick and Flea').exclude(quantity=0)
            
        if forms.initial['disease'] == '1st dose Bordetella Bronchiseptica Bacterin' or forms.initial['disease'] == '2nd dose Bordetella Bronchiseptica Bacterin':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Bordetella Bronchiseptica Bacterin').exclude(quantity=0)
            
        if forms.initial['disease'] == '1st dose DHPPiL4 Vaccination' or forms.initial['disease'] == '2nd dose DHPPiL4 Vaccination':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='DHPPiL4').exclude(quantity=0)
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'health_data':health_data,
        'phyexam_data':phyexam_data,
        'formset':formset,
        'age': data.age_days,
        'vu':vu,
        'style':style,
        'active_1':active_1,
        'active_2':active_2,
        'active_3':active_3,
        'title':'Health Record of ' + str(data),
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
    user = user_session(request)
    data = K9.objects.get(name='Testing')
    vr = VaccinceRecord.objects.get(k9=data)
    vu = VaccineUsed.objects.filter(vaccine_record=vr)
    style = 'ui green message'

    VaccinationUsedFormset= inlineformset_factory(VaccinceRecord, VaccineUsed, form=VaccinationUsedForm, extra=0)
    formset = VaccinationUsedFormset(request.POST or None, request.FILES or None, prefix='record', instance=vr)

    ctr=0
    ctr1=0
    for forms in formset:
        if forms.initial['disease'] == '1st Deworming' or forms.initial['disease'] == '2nd Deworming' or forms.initial['disease'] == '3rd Deworming' or forms.initial['disease'] == '4th Deworming':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Deworming').exclude(quantity=0)
           
        if forms.initial['disease'] == '1st dose DHPPiL+CV Vaccination' or forms.initial['disease'] == '2nd dose DHPPiL+CV Vaccination' or forms.initial['disease'] == '3rd dose DHPPiL+CV Vaccination':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='DHPPiL+CV').exclude(quantity=0)

        if forms.initial['disease'] == '1st Heartworm Prevention' or forms.initial['disease'] == '2nd Heartworm Prevention' or forms.initial['disease'] == '3rd Heartworm Prevention' or forms.initial['disease'] == '4th Heartworm Prevention' or forms.initial['disease'] == '5th Heartworm Prevention' or forms.initial['disease'] == '6th Heartworm Prevention' or forms.initial['disease'] == '7th Heartworm Prevention' or forms.initial['disease'] == '8th Heartworm Prevention':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Heartworm').exclude(quantity=0)

        if forms.initial['disease'] == 'Anti-Rabies Vaccination':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Anti-Rabies').exclude(quantity=0)
            
        if forms.initial['disease'] == '1st Tick and Flea Prevention' or forms.initial['disease'] == '2nd Tick and Flea Prevention' or forms.initial['disease'] == '3rd Tick and Flea Prevention' or forms.initial['disease'] == '4th Tick and Flea Prevention' or forms.initial['disease'] == '5th Tick and Flea Prevention' or forms.initial['disease'] == '6th Tick and Flea Prevention' or forms.initial['disease'] == '7th Tick and Flea Prevention':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Tick and Flea').exclude(quantity=0)
            
        if forms.initial['disease'] == '1st dose Bordetella Bronchiseptica Bacterin' or forms.initial['disease'] == '2nd dose Bordetella Bronchiseptica Bacterin':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Bordetella Bronchiseptica Bacterin').exclude(quantity=0)
            
        if forms.initial['disease'] == '1st dose DHPPiL4 Vaccination' or forms.initial['disease'] == '2nd dose DHPPiL4 Vaccination':
            forms.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='DHPPiL4').exclude(quantity=0)

    if request.method == 'POST':
        formset = VaccinationUsedFormset(request.POST, request.FILES, prefix='record', instance=vr)
        
        if formset.is_valid():
            for forms in formset:
                if forms.is_valid():
                    f = forms.save(commit=False)
                    if f.vaccine != None and f.date_vaccinated != None and f.done == False:  
                        f.veterinary = user
                        f.done = True
                        f.save()

                        ctr1=ctr1+1
                        
                        if f.disease == '1st Deworming':
                            vr.deworming_1 = True
                        elif f.disease == '2nd Deworming':
                            vr.deworming_2 = True
                        elif f.disease == '3rd Deworming':
                            vr.deworming_3 = True
                        elif f.disease == '1st dose DHPPiL+CV Vaccination':
                            vr.dhppil_cv_1 = True
                        elif f.disease == '1st Heartworm Prevention':
                            vr.heartworm_1 = True
                        elif f.disease == '1st dose Bordetella Bronchiseptica Bacterin':
                            vr.bordetella_1 = True
                        elif f.disease == '1st Tick and Flea Prevention':
                            vr.tick_flea_1 = True
                        elif f.disease == '2nd dose DHPPiL+CV Vaccination':
                            vr.dhppil_cv_2 = True
                        elif f.disease == '4th Deworming':
                            vr.deworming_4 = True
                        elif f.disease == '2nd Heartworm Prevention':
                            vr.heartworm_2 = True
                        elif f.disease == '2nd dose Bordetella Bronchiseptica Bacterin':
                            vr.bordetella_2 = True
                        elif f.disease == 'Anti-Rabies Vaccination	':
                            vr.anti_rabies = True
                        elif f.disease == '2nd Tick and Flea Prevention':
                            vr.tick_flea_2 = True
                        elif f.disease == '3rd dose DHPPiL+CV Vaccination':
                            vr.dhppil_cv_3 = True
                        elif f.disease == '3rd Heartworm Prevention':
                            vr.heartworm_3 = True
                        elif f.disease == '1st dose DHPPiL4 Vaccination':
                            vr.dhppil4_1 = True
                        elif f.disease == '3rd Tick and Flea Prevention':
                            vr.tick_flea_3 = True
                        elif f.disease == '2nd dose DHPPiL4 Vaccination':
                            vr.dhppil4_2 = True
                        elif f.disease == '4th Heartworm Prevention':
                            vr.heartworm_4 = True
                        elif f.disease == '4th Tick and Flea Prevention':
                            vr.tick_flea_4 = True
                        elif f.disease == '5th Heartworm Prevention':
                            vr.heartworm_5 = True
                        elif f.disease == '6th Heartworm Prevention':
                            vr.heartworm_6 = True
                        elif f.disease == '2nd dose DHPPiL4 Vaccination':
                            vr.bordetella_2 = True
                        elif f.disease == '6th Tick and Flea Prevention':
                            vr.tick_flea_6 = True
                        elif f.disease == '7th Heartworm Prevention':
                            vr.heartworm_7 = True
                        elif f.disease == '7th Tick and Flea Prevention':
                            vr.tick_flea_7 = True
                        elif f.disease == '8th Heartworm Prevention':
                            vr.heartworm_8 = True
                        vr.save()
                        
                    else: 
                        pass
                        
                    if f.image != None:
                        ctr1=ctr1+1
                        f.save(update_fields=["image"])

                    if f.done == False and f.vaccine != None and f.date_vaccinated == None:
                        ctr = ctr+1
                    elif f.done == False and f.vaccine == None and f.date_vaccinated != None:
                        ctr = ctr+1

            print(ctr1)
            if ctr1>0:
                messages.success(request, 'Prevention Updated!')
                return redirect('unitmanagement:vaccination_form')

            if ctr>0:
                messages.success(request, 'Incomplete input. Please check again.')
                style='ui red message'
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'formset':formset,
        'vu':vu,
        'style':style,
        'title':'Health Record of ' + str(data),
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
    user = user_session(request)
    form = K9IncidentForm(request.POST or None)
    dog = K9.objects.get(handler=user)
    form.fields['k9'].queryset = K9.objects.filter(handler=user)
    style=''

    num = K9_Incident.objects.filter(reported_by=str(user)).filter(status='Pending').exclude(incident='Sick').count()
    incident = K9_Incident.objects.filter(reported_by=str(user)).filter(status='Pending').exclude(incident='Sick')

    if request.method == "POST":
        if form.is_valid():
            f = form.save(commit=False)
            f.reported_by = user
            f.save()

            dog.status = f.incident
            dog.save()

            return redirect('unitmanagement:k9_incident')
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'title': "K9 Incident",
        'actiontype': "Submit",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'num':num,
        'incident':incident,
    }
    return render (request, 'unitmanagement/k9_incident.html', context)

# TODO
def k9_incident_list(request):
    style='ui green message'
    data = K9_Incident.objects.filter(status='Pending').exclude(incident='Sick').exclude(incident='Accident')
    
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "K9 Incident List",
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data':data,
    }
    return render (request, 'unitmanagement/k9_incident_list.html', context)

def k9_sick_form(request):
    user = user_session(request)
    form = K9IncidentForm(request.POST or None, request.FILES or None)
    style='ui green message'

    handler = K9.objects.filter(handler=user)
    form.fields['k9'].queryset =  handler

    if request.method == "POST":
        if form.is_valid():
            form = form.save(commit=False)
            form.incident = 'Sick'
            form.reported_by = user
            form.k9.status = form.incident
            form.save()

            files = request.FILES.getlist('image_file')

            for f in files:
                Image.objects.create(incident_id=form, image=f)

            style = "ui green message"
            messages.success(request, 'Health Concern has been successfully Reported!')
            return redirect('unitmanagement:k9_sick_form') 

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
            

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'title': "K9 Health Form",
        'actiontype': "Submit",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'handler': handler,
    }
    return render (request, 'unitmanagement/k9_sick_form.html', context)

def k9_retreived(request, id):
    data = K9_Incident.objects.get(id=id)
    data.status = 'Done'
    data.k9.status = 'Working Dog'
    data.save()
    messages.success(request, 'K9 retrieval has been confirmed and data has been updated!')
    return redirect('unitmanagement:k9_incident_list') 

def health_list_handler(request):
    user = user_session(request)
    style = "ui green message"
    k9 = K9.objects.get(handler=user)
    date = dt.date.today()
    data_arr = []

    if user.position == 'Handler':
        data = K9_Incident.objects.filter(reported_by=user).filter(status='Pending')
        data2 = Health.objects.filter(dog=k9).filter(status='On-Going')

    for da in data2:
        d =  da.date_done - dt.date.today()
        d = d.days
        data_arr.append(d)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'title': "Health Concern List",
        'actiontype': "Submit",
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data':data,
        'data2':data2,
        'date':date,
        'data_arr':data_arr,
    }
    return render (request, 'unitmanagement/health_list_handler.html', context)

def handler_incident_form(request):
    user = user_session(request)
    form = HandlerIncidentForm(request.POST or None)
    style='ui green message'
    
    data = Team_Assignment.objects.get(team_leader=user)

    team = Team_Dog_Deployed.objects.filter(team_assignment=data).filter(status='Deployed')
    handler = []
    for team in team:
        handler.append(team.handler.id)

    form.fields['handler'].queryset = User.objects.filter(id__in=handler)
    if request.method == "POST":
        if form.is_valid():
            a = request.POST['k9_select']
            b = K9.objects.get(name = a)
            f = form.save(commit=False)
            f.reported_by = user
            f.k9 = b
            f.save()

            style = "ui green message"
            messages.success(request, 'Incident has been successfully Reported!')
            return redirect('unitmanagement:handler_incident_form') 

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
    return render (request, 'unitmanagement/handler_incident_form.html', context)

def on_leave_request(request):
    user = user_session(request)
    form = HandlerOnLeaveForm(request.POST or None)
    style=''
    form.fields['handler'].queryset = User.objects.filter(id=user.id)
    
    data = Handler_On_Leave.objects.filter(handler=user).filter(status='Pending').filter(incident='On-Leave')
    num = Handler_On_Leave.objects.filter(handler=user).filter(status='Pending').filter(incident='On-Leave').count()

    if request.method == "POST":
        if form.is_valid():
            incident_save = form.save()
            
            form = HandlerOnLeaveForm()
            style = "ui green message"
            messages.success(request, 'Request has been successfully Submited!')
            return redirect('unitmanagement:on_leave_request')
        
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'title': "On-Leave Form",
        'actiontype': "Submit",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data':data,
        'num':num,
    }
    return render (request, 'unitmanagement/on_leave_form.html', context)

def reassign_assets(request):
    style=''
    form = ReassignAssetsForm(request.POST or None)
    k9 = K9.objects.filter(training_status='For-Deployment').filter(handler=None)
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
    style='ui green message'
    data1 = Handler_On_Leave.objects.filter(status='Pending').filter(incident='On-Leave') 
    data2 = Handler_On_Leave.objects.filter(status='Approved').filter(incident='On-Leave') 

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
def on_leave_decision(request, id):
    user = user_session(request)
    data = Handler_On_Leave.objects.get(id=id)
    leave = request.GET.get('leave')

    if leave == 'approve':
        data.status = 'Approved'
        data.handler.status = 'On-Leave'
        data.approved_by = user
    elif leave == 'deny':
        data.status = 'Denied'
    
    data.save()

    messages.success(request, 'You have ' + str(data.status) + ' ' + str(data.handler) + 's Leave Request.')
    return redirect('unitmanagement:on_leave_list')

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
    data = K9.objects.filter(training_status='For-Deployment').filter(handler=None)
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Unpartnered K9 List",
        'data':data,
        'style':style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/k9_unpartnered_list.html', context)

# TODO 
# choose_handler Cycle
def choose_handler_list(request, id):
    form = assign_handler_form(request.POST or None)
    style = ""
    k9 = K9.objects.get(id=id)  

    handler = User.objects.filter(status='Working').filter(position='Handler').filter(partnered=False)
    g = []
    for h in handler:
        c = Handler_K9_History.objects.filter(handler=h).filter(k9__capability=k9.capability).count()
        g.append(c)

    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            f = form.save(commit=False)
            f.k9 = k9
            f.save()
            
            #K9 Update
            k9.training_status = 'On-Training'
            k9.handler = f.handler
            k9.save()

            #Handler Update
            h = User.objects.get(id= f.handler.id)
            h.partnered = True
            h.save()

            messages.success(request, str(k9) + ' has been assigned to ' + str(h))
            return redirect('unitmanagement:k9_unpartnered_list')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    
    context = {
        'Title': "K9 Assignment for " + k9.name,
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'k9':k9,
        'g':g,
    }
    return render (request, 'unitmanagement/choose_handler_list.html', context)

# TODO 
# choose_handler Cycle
def choose_handler(request, id):
    k9_id_partnered = request.session["k9_id_partnered"]
    k9 = K9.objects.get(id=k9_id_partnered)
    handler = User.objects.get(id=id)

    k9.handler = handler
    k9.save()

    handler.partnered = True
    handler.save()

    Handler_K9_History.objects.create(k9=k9, handler=handler)
    messages.success(request, k9.name + ' and ' + handler.fullname + ' has been successfully Partnered!')
     
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
    image = Image.objects.filter(incident_id=data)

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

            health = form.save(commit=False)
            health.dog = data.k9
            health.incident_id = data
            health.veterinary = user_in_session
            health.save()
            new_form = health.pk
            form_instance = Health.objects.get(id=new_form)
            dog = K9.objects.get(id=health.dog.id)
            
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

                    for form in formset:
                        f = form.save()
                        med = Medicine_Inventory.objects.get(id=f.medicine.id)
                        print('Med: ', med)
                        med.quantity = med.quantity - f.quantity
                        med.save()
                        Medicine_Subtracted_Trail.objects.create(inventory = med, user=user_in_session, quantity = f.quantity)
                        
                    print('Days: ',max(days))
                    print('Health: ', health)
                    health.duration =  max(days)
                    health.save() #health instance
                    dog.status = 'Sick'
                    data.status= 'Done'
                    dog.save() #k9 instance
                    data.save() #incident instance
                    style = "ui green message"
                    messages.success(request, 'You have replied to a health concern!')
                    return redirect('unitmanagement:k9_sick_list')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': data.k9,
        'image':image,
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
        data = K9.objects.all()
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
        data = User.objects.all()
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

def load_handler(request):

    handler = None

    try:
        handler_id = request.GET.get('handler')
        handler = User.objects.get(id=handler_id)
        pi = Personal_Info.objects.get(UserID=handler)
        edd = Handler_K9_History.objects.filter(handler=handler).filter(k9__capability='EDD').count()
        ndd = Handler_K9_History.objects.filter(handler=handler).filter(k9__capability='NDD').count()
        sar = Handler_K9_History.objects.filter(handler=handler).filter(k9__capability='SAR').count()
        
    except:
        pass

    context = {
        'handler': handler,
        'pi':pi,
        'ndd':ndd,
        'edd':edd,
        'sar':sar,
    }

    return render(request, 'training/handler_data.html', context)

def load_stamp(request):

    stamp = None

    try:
        stamp_id = request.GET.get('stamp')
        stamp = VaccineUsed.objects.get(id=stamp_id)

    except:
        pass

    context = {
        'stamp': stamp,
    }

    return render(request, 'unitmanagement/stamp_data.html', context)

def load_k9(request):

    k9 = None

    try:
        handler_id = request.GET.get('handler')
        k9 = K9.objects.get(handler__id=handler_id) 
    except:
        pass

    context = {
        'k9': k9,
    }

    return render(request, 'unitmanagement/k9_data.html', context)