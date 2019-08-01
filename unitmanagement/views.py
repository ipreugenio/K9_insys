from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.db.models import aggregates
from django.contrib import messages
import datetime as dt
from datetime import timedelta, date, datetime
from decimal import Decimal
import itertools
from django.db.models import Sum, Avg, Max, Q
from django.core.exceptions import ObjectDoesNotExist
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse

from planningandacquiring.forms import k9_detail_form
from planningandacquiring.models import K9

from unitmanagement.models import PhysicalExam, Health, HealthMedicine, K9_Incident, Handler_On_Leave, K9_Incident, Handler_K9_History, Medicine_Request, Food_Request, Miscellaneous_Request, Request_Transfer,Call_Back_K9, Handler_Incident, Replenishment_Request
from unitmanagement.forms import PhysicalExamForm, HealthForm, HealthMedicineForm, VaccinationRecordForm, HandlerOnLeaveForm, RequestMiscellaneous, RequestFood, RequestMedicine

from unitmanagement.forms import K9IncidentForm, HandlerIncidentForm, VaccinationUsedForm, ReassignAssetsForm, ReproductiveForm, RequestTransferForm, ReplenishmentForm
from inventory.models import Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Miscellaneous_Subtracted_Trail, Miscellaneous
from inventory.models import Medicine_Received_Trail, Food_Subtracted_Trail, Food
from unitmanagement.models import HealthMedicine, Health, VaccinceRecord, VaccineUsed, Notification
from deployment.models import K9_Schedule, Dog_Request, Team_Dog_Deployed, Team_Assignment

from unitmanagement.models import PhysicalExam, Health, HealthMedicine, K9_Incident, Handler_On_Leave, K9_Incident, Handler_K9_History
from unitmanagement.forms import PhysicalExamForm, HealthForm, HealthMedicineForm, VaccinationRecordForm, HandlerOnLeaveForm
from unitmanagement.forms import K9IncidentForm, HandlerIncidentForm, VaccinationUsedForm, ReassignAssetsForm, ReproductiveForm, DateForm

from inventory.models import Medicine_Received_Trail, Food_Subtracted_Trail, Food
from unitmanagement.models import HealthMedicine, Health, VaccinceRecord,VaccineUsed, Notification, Image, VaccinceRecord, Transaction_Health
from deployment.models import K9_Schedule, Dog_Request, Team_Dog_Deployed, Team_Assignment, Incidents, Daily_Refresher, Area, Location, TempCheckup

from profiles.models import User, Account, Personal_Info
from training.models import K9_Handler, Training_History,Training_Schedule, Training
from training.forms import assign_handler_form

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from unitmanagement.serializers import K9Serializer
from django.db.models import Q
from dateutil.parser import parse
# Create your views here.

import json

from pandas import DataFrame as df

def notif(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)

    if user_in_session.position == 'Veterinarian':
        notif = Notification.objects.filter(position='Veterinarian').order_by('-datetime')
    elif user_in_session.position == 'Handler':
        notif = Notification.objects.filter(user=user_in_session).order_by('-datetime').exclude(notif_type='handler_on_leave').exclude(notif_type='handler_died')
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
    elif notif.notif_type == 'handler_on_leave' :
        notif.viewed = True
        notif.save()
        return redirect('unitmanagement:on_leave_details', id = notif.other_id)
    #TODO location incident view details
    elif notif.notif_type == 'location_incident' :
        notif.viewed = True
        notif.save()
        return redirect('deployment:incident_detail', id = notif.other_id)


def index(request):
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    #form = VaccinationYearlyForm

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,

    }
    return render (request, 'unitmanagement/index.html', context)


def yearly_vaccine_list(request):
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    vr = VaccinceRecord.objects.filter(deworming_4=True,dhppil_cv_3=True,anti_rabies=True,bordetella_2=True,dhppil4_2=True)

    list_k9 = []

    for v in vr:
        list_k9.append(v.k9.id)

    k9 = K9.objects.exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").filter(id__in=list_k9)

    k9_ar = []
    k9_dh = []
    k9_br = []
    k9_dw = []

    for k9 in k9:
        try:
            ar = VaccineUsed.objects.filter(disease__contains='Anti-Rabies').filter(k9=k9).latest('date_vaccinated')
            nxt_ar = ar.date_vaccinated + relativedelta(years=+1)
        except:
            dar = k9.date_created + relativedelta(months=+6)
            nxt_ar = dar

        try:
            br = VaccineUsed.objects.filter(disease__contains='Bordetella').filter(k9=k9).latest('date_vaccinated')
            nxt_br = br.date_vaccinated + relativedelta(years=+1)
        except:
            dbr = k9.date_created + relativedelta(months=+6)
            nxt_br = dbr

        try:
            dh = VaccineUsed.objects.filter(disease__contains='DHPPiL4').filter(k9=k9).latest('date_vaccinated')
            nxt_dh = dh.date_vaccinated + relativedelta(years=+1)
        except:
            ddh = k9.date_created + relativedelta(months=+6)
            nxt_dh = ddh

        try:
            dw = VaccineUsed.objects.filter(disease__contains='Deworming').filter(k9=k9).latest('date_vaccinated')
            nxt_dw = dw.date_vaccinated + relativedelta(months=+1)
        except:
            ddw = k9.date_created + relativedelta(months=+6)
            nxt_dw = ddw

        if nxt_ar <= dt.date.today():
            ard = [k9,nxt_ar]
            k9_ar.append(ard)
        if nxt_br <= dt.date.today():
            brd = [k9,nxt_br]
            k9_br.append(brd)
        if nxt_dh <= dt.date.today():
            dhd = [k9,nxt_dh]
            k9_dh.append(dhd)
        if nxt_dw <= dt.date.today():
            dwd = [k9,nxt_dw]
            k9_dw.append(dwd)

    form = VaccinationUsedForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            id = request.POST.get('k9')
            k9 = K9.objects.get(id=id)

            f = form.save(commit=False)
            f.veterinary = user
            f.done = True
            f.disease = request.POST.get('type')
            f.k9 = k9

            #minus
            mi = Medicine_Inventory.objects.get(vaccine=f.vaccine)
            mi.quantity = mi.quantity - 1

            if mi.quantity > 0 :
                f.save()
                mi.save()
                messages.success(request, str(f.k9) + ' has been given ' + str(f.vaccine))
            else:
                messages.warning(request, 'Insufficient Quantity')
            return redirect('unitmanagement:yearly_vaccine_list')

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'form':form,
        'k9_ar':k9_ar,
        'k9_dh':k9_dh,
        'k9_br':k9_br,
        'k9_dw':k9_dw,
        'count_ar':len(k9_ar),
        'count_dh':len(k9_dh),
        'count_br':len(k9_br),
        'count_dw':len(k9_dw),
    }
    return render (request, 'unitmanagement/yearly_vaccination.html', context)

def vaccination_list(request):
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    k9_ar = []
    k9_dh = []
    k9_br = []
    k9_dw = []
    k9_hw = []
    k9_d4 = []
    k9_tf = []

    vr = VaccinceRecord.objects.filter(status='Pending')
    for vr in vr:
        #2 weeks
        if vr.deworming_1 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=14:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='1st Deworming')
                dwd = [k9,vu]
                k9_dw.append(dwd)
        #4 weeks
        if vr.deworming_2 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=24:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='2nd Deworming')
                dwd = [k9,vu]
                k9_dw.append(dwd)
        #6 weeks
        if vr.deworming_3 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=42:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='3rd Deworming')
                dwd = [k9,vu]
                k9_dw.append(dwd)
        #6 weeks
        if vr.dhppil_cv_1 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=42:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='1st dose DHPPiL+CV Vaccination')
                dwd = [k9,vu]
                k9_dh.append(dwd)
        #6 weeks
        if vr.heartworm_1 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=42:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='1st Heartworm Prevention')
                dwd = [k9,vu]
                k9_hw.append(dwd)
        #8 weeks
        if vr.bordetella_1 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=56:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='1st dose Bordetella Bronchiseptica Bacterin')
                dwd = [k9,vu]
                k9_br.append(dwd)
        #8 weeks
        if vr.tick_flea_1 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=42:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='1st Tick and Flea Prevention')
                dwd = [k9,vu]
                k9_tf.append(dwd)
        
        #9 weeks
        if vr.dhppil_cv_2 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=63:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='2nd dose DHPPiL+CV')
                dwd = [k9,vu]
                k9_dh.append(dwd)
        #9 weeks
        if vr.deworming_3 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=63:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='4th Deworming')
                dwd = [k9,vu]
                k9_tf.append(dwd)

        #10 weeks
        if vr.heartworm_2 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=63:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='2nd Heartworm Prevention')
                dwd = [k9,vu]
                k9_hw.append(dwd)
        #11 weeks
        if vr.bordetella_2 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=63:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='2nd dose Bordetella Bronchiseptica Bacterin')
                dwd = [k9,vu]
                k9_br.append(dwd)
        #12 weeks
        if vr.anti_rabies == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=84:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='Anti-Rabies Vaccination')
                dwd = [k9,vu]
                k9_ar.append(dwd)

        #12 weeks
        if vr.tick_flea_2 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=84:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='2nd Tick and Flea Prevention')
                dwd = [k9,vu]
                k9_hw.append(dwd)
        #12 weeks
        if vr.dhppil_cv_3 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=84:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='3rd dose DHPPiL+CV Vaccination')
                dwd = [k9,vu]
                k9_dh.append(dwd)
        
        #14 weeks
        if vr.heartworm_3 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=98:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='3rd Heartworm Prevention')
                dwd = [k9,vu]
                k9_hw.append(dwd)

        #15 weeks
        if vr.dhppil4_1 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=105:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='1st dose DHPPiL4 Vaccination')
                dwd = [k9,vu]
                k9_d4.append(dwd)
        #16 weeks
        if vr.tick_flea_3 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=112:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='3rd Tick and Flea Prevention')
                dwd = [k9,vu]
                k9_tf.append(dwd)
        
        #18 weeks
        if vr.dhppil4_2 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=126:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='2nd dose DHPPiL4 Vaccination')
                dwd = [k9,vu]
                k9_d4.append(dwd)
        #18 weeks
        if vr.heartworm_4 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=126:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='4th Heartworm Prevention')
                dwd = [k9,vu]
                k9_hw.append(dwd)

        #20 weeks
        if vr.tick_flea_4 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=140:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='4th Tick and Flea Prevention')
                dwd = [k9,vu]
                k9_tf.append(dwd)
        #22 weeks
        if vr.heartworm_5 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=154:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='5th Heartworm Prevention')
                dwd = [k9,vu]
                k9_hw.append(dwd)

        #24 weeks
        if vr.tick_flea_5 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=168:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='5th Tick and Flea Prevention')
                dwd = [k9,vu]
                k9_tf.append(dwd)
        #26 weeks
        if vr.heartworm_6 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=182:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='6th Heartworm Prevention')
                dwd = [k9,vu]
                k9_hw.append(dwd)
        
        #28 weeks
        if vr.tick_flea_6 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=196:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='6th Tick and Flea Prevention')
                dwd = [k9,vu]
                k9_tf.append(dwd)

        #30 weeks
        if vr.heartworm_7 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=210:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='7th Heartworm Prevention')
                dwd = [k9,vu]
                k9_hw.append(dwd)
        #32 weeks
        if vr.tick_flea_7 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=224:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='7th Tick and Flea Prevention')
                dwd = [k9,vu]
                k9_tf.append(dwd)
        
        #34 weeks
        if vr.heartworm_8 == False:
            k9 = K9.objects.get(id=vr.k9.id)
            if k9.age_days >=238:
                vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease='8th Heartworm Prevention')
                dwd = [k9,vu]
                k9_hw.append(dwd)


    form = VaccinationUsedForm(request.POST or None, request.FILES or None)

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'form':form,
        'k9_ar':k9_ar,
        'k9_dh':k9_dh,
        'k9_br':k9_br,
        'k9_dw':k9_dw,
        'k9_hw':k9_hw,
        'k9_d4':k9_d4,
        'k9_tf':k9_tf,
        'count_ar':len(k9_ar),
        'count_dh':len(k9_dh),
        'count_br':len(k9_br),
        'count_dw':len(k9_dw),
        'count_hw':len(k9_hw),
        'count_d4':len(k9_d4),
        'count_tf':len(k9_tf),
    }
    return render (request, 'unitmanagement/vaccination_list.html', context)

def vaccine_submit(request):
    user = user_session(request)
    form = VaccinationUsedForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        #print(form)
        if form.is_valid():
            id = request.POST.get('k9')
            k9 = K9.objects.get(id=id)
            vr = VaccinceRecord.objects.get(k9=k9)
            disease = request.POST.get('disease')

            f = form.save(commit=False)
            
            vu = VaccineUsed.objects.filter(vaccine_record=vr).get(disease=disease)
            vu.veterinary = user
            vu.vaccine = f.vaccine
            vu.date_vaccinated = f.date_vaccinated
            vu.veterinary = user
            vu.image = f.image
            
            if vu.disease == '1st Deworming':
                vr.deworming_1 = True
            elif vu.disease == '2nd Deworming':
                vr.deworming_2 = True
            elif vu.disease == '3rd Deworming':
                vr.deworming_3 = True
            elif vu.disease == '1st dose DHPPiL+CV Vaccination':
                vr.dhppil_cv_1 = True
            elif vu.disease == '1st Heartworm Prevention':
                vr.heartworm_1 = True
            elif vu.disease == '1st dose Bordetella Bronchiseptica Bacterin':
                vr.bordetella_1 = True
            elif vu.disease == '1st Tick and Flea Prevention':
                vr.tick_flea_1 = True
            elif vu.disease == '2nd dose DHPPiL+CV Vaccination':
                vr.dhppil_cv_2 = True
            elif vu.disease == '4th Deworming':
                vr.deworming_4 = True
            elif vu.disease == '2nd Heartworm Prevention':
                vr.heartworm_2 = True
            elif vu.disease == '2nd dose Bordetella Bronchiseptica Bacterin':
                vr.bordetella_2 = True
            elif vu.disease == 'Anti-Rabies Vaccination	':
                vr.anti_rabies = True
            elif vu.disease == '2nd Tick and Flea Prevention':
                vr.tick_flea_2 = True
            elif vu.disease == '3rd dose DHPPiL+CV Vaccination':
                vr.dhppil_cv_3 = True
            elif vu.disease == '3rd Heartworm Prevention':
                vr.heartworm_3 = True
            elif vu.disease == '1st dose DHPPiL4 Vaccination':
                vr.dhppil4_1 = True
            elif vu.disease == '3rd Tick and Flea Prevention':
                vr.tick_flea_3 = True
            elif vu.disease == '2nd dose DHPPiL4 Vaccination':
                vr.dhppil4_2 = True
            elif vu.disease == '4th Heartworm Prevention':
                vr.heartworm_4 = True
            elif vu.disease == '4th Tick and Flea Prevention':
                vr.tick_flea_4 = True
            elif vu.disease == '5th Heartworm Prevention':
                vr.heartworm_5 = True
            elif vu.disease == '5th Tick and Flea Prevention':
                vr.tick_flea_5 = True
            elif vu.disease == '6th Heartworm Prevention':
                vr.heartworm_6 = True
            elif vu.disease == '6th Tick and Flea Prevention':
                vr.tick_flea_6 = True
            elif vu.disease == '7th Heartworm Prevention':
                vr.heartworm_7 = True
            elif vu.disease == '7th Tick and Flea Prevention':
                vr.tick_flea_7 = True
            elif vu.disease == '8th Heartworm Prevention':
                vr.heartworm_8 = True
         
            #minus
            mi = Medicine_Inventory.objects.get(id=vu.vaccine.id)
            mi.quantity = mi.quantity - 1

            if mi.quantity > 0 :
                vu.save()
                vr.save()
                mi.save()

            messages.success(request, str(k9) + ' has been given ' + str(f.vaccine))
            return HttpResponseRedirect('vaccination-list')
        else:
            messages.warning(request, 'Insufficient Quantity')
            return HttpResponseRedirect('vaccination-list')    



#TODO Initialize treatment
#TODO fix missing form
def health_form(request):
    form = HealthForm(request.POST or None, request.FILES or None)

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
                    dog.save()

                    minus_list = zip(form_med, form_quantity)

                    # subtract item
                    for a, b in minus_list:
                        mm = Medicine_Inventory.objects.get(id=a.id)
                        mm.quantity = mm.quantity - b
                        mm.save()
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
def physical_exam_form(request, id=None):
    form = PhysicalExamForm(request.POST or None)
    user_serial = request.session['session_serial']
    user_s = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user_s.UserID.id)

    if 'phex_k9_id' in request.session:
        form.initial['dog'] = K9.objects.get(id=request.session['phex_k9_id'])

    if id:
        k9 = K9.objects.get(id = id)
        form.initial['dog'] = k9
        form.fields['dog'].queryset =  K9.objects.filter(id=id)
        # form.fields['dog'].widget.attrs['disabled'] = True

    style=""
    if request.method == 'POST':
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.date_next_exam = dt.date.today() + relativedelta(months=+3)
            new_form.user = current_user
            new_form.body_score = request.POST.get('radio_select')

            bs = int(new_form.body_score)
            k9 = K9.objects.get(id=new_form.dog.id)

            if bs == 1 | bs == 5:
                k9.fit = False
            else:
                k9.fit = True

            new_form.save()
            k9.save()

            style = "ui green message"
            messages.success(request, 'Physical Exam for ' + str(k9) + ' has been successfully recorded!')
            form = PhysicalExamForm()

            if id:
                return redirect('unitmanagement:k9_checkup_list_today')

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

def unfit_list(request):
    k9 = K9.objects.filter(fit=False)
    form = PhysicalExamForm(request.POST or None)
    user = user_session(request)

    data = []
    for k9 in k9:
        try:
            phex = PhysicalExam.objects.filter(dog=k9).latest('date')
            arr = [k9,phex.date]
            data.append(arr)
        except:
            pass

    if request.method == 'POST':
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.date_next_exam = dt.date.today() + relativedelta(months=+3)
            new_form.user = user
            new_form.body_score = request.POST.get('radio_select')

            bs = int(new_form.body_score)
            k9 = K9.objects.get(id=new_form.dog.id)

            if bs == 1 | bs == 5:
                k9.fit = False
            else:
                k9.fit = True

            new_form.save()
            k9.save()

            style = "ui green message"
            messages.success(request, 'Physical Exam has been successfully recorded!')

            return redirect('unitmanagement:unfit_list')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data': data,
    }
    return render (request, 'unitmanagement/unfit_list.html', context)

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
                        elif f.disease == '5th Tick and Flea Prevention':
                            vr.tick_flea_5 = True
                        elif f.disease == '6th Heartworm Prevention':
                            vr.heartworm_6 = True
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
        'data':data,
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

def health_history_handler(request):
    user_serial = request.session['session_serial']
    user_s = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user_s.UserID.id)

    data = None
    try:
        data = K9.objects.get(handler=current_user)
    except: pass
    health_data = Health.objects.filter(dog = data).order_by('-date')
    phyexam_data = PhysicalExam.objects.filter(dog = data).order_by('-date')

    vr = None
    vu = None
    try:
        vr = VaccinceRecord.objects.get(k9=data)
        vu = VaccineUsed.objects.filter(vaccine_record=vr)
    except: pass
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

    age = None
    try:
        age = data.age_days
    except: pass
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'health_data':health_data,
        'phyexam_data':phyexam_data,
        'formset':formset,
        'data':data,
        'age': age,
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


    th = Transaction_Health.objects.filter(health=data).filter(status='Pending')

    image = None
    for t in th:
        image = Image.objects.filter(incident_id=t.follow_up)

    print(data.follow_up_done, data.follow_up)
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
        'th':th,
        'image':image,
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

# def requests_form(request):
#     style=""

#     medicine_formset = formset_factory(RequestMedicine, extra=1, can_delete=True)
#     food_formset = formset_factory(RequestFood, extra=1, can_delete=True)
#     equipment_formset = formset_factory(RequestEquipment, extra=1, can_delete=True)

#     if request.method == "POST":
#         # print(form)
#         formset1 = medicine_formset(request.POST or None)
#         formset2 = food_formset(request.POST or None)
#         formset3 = equipment_formset(request.POST or None)

#         med = []
#         med_quantity = []
#         equipment = []
#         equipment_quantity = []
#         food = []
#         food_quantity = []

#         if formset1.is_valid():
#             for form in formset1:
#                 m = Medicine.objects.get(medicine_fullname=form.cleaned_data['medicine']).filter()
#                 med.append(m)
#                 med_quantity.append(form.cleaned_data['quantity'])
#                 mi = Medicine_Inventory.objects.filter(medicine__in=med)

#         if formset2.is_valid():
#             for form in formset1:
#                 f = Food.objects.get(food_fullname=form.cleaned_data['food']).filter()
#                 food.append(f)
#                 food_quantity.append(form.cleaned_data['quantity'])



#     notif_data = notif(request)
#     count = notif_data.filter(viewed=False).count()
#     user = user_session(request)
#     context = {
#         'title': "Replenish Assets",
#         'actiontype': "Submit",
#         'style': style,
#         'formset1': medicine_formset(),
#         'formset2': food_formset(),
#         'formset3': equipment_formset(),
#         'notif_data':notif_data,
#         'count':count,
#         'user':user,
#     }
#     return render (request, 'unitmanagement/request_form.html', context)

def trained_list(request):
    # k9s_for_grading = []
    # train_sched = Training_Schedule.objects.exclude(date_start=None).exclude(date_end=None)
    #
    # for item in train_sched:
    #     if item.k9.training_level == item.stage:
    #         k9s_for_grading.append(item.k9.id)

    # data = K9.objects.filter(id__in=k9s_for_grading)

    data = K9.objects.filter(training_status = "Trained")

    NDD_count = K9.objects.filter(capability='NDD').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()
    EDD_count = K9.objects.filter(capability='EDD').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()
    SAR_count = K9.objects.filter(capability='SAR').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()

    NDD_demand = list(Team_Assignment.objects.aggregate(Sum('NDD_demand')).values())[0]
    EDD_demand = list(Team_Assignment.objects.aggregate(Sum('EDD_demand')).values())[0]
    SAR_demand = list(Team_Assignment.objects.aggregate(Sum('SAR_demand')).values())[0]

    if not NDD_demand:
        NDD_demand = 0
    if not EDD_demand:
        EDD_demand = 0
    if not SAR_demand:
        SAR_demand = 0

    # breed = ['Belgian Malinois','Dutch Sheperd','German Sheperd','Golden Retriever','Jack Russel','Labrador Retriever']

    # for breed in breed:

    #Belgian Malinois
    bm_m = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Belgian Malinois').filter(sex='Male').count()
    bm_f = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Belgian Malinois').filter(sex='Female').count()

    bm_m_edd =  K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Belgian Malinois').filter(capability='EDD').filter(sex='Male').count()
    bm_m_ndd =  K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Belgian Malinois').filter(capability='NDD').filter(sex='Male').count()
    bm_m_sar =  K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Belgian Malinois').filter(capability='SAR').filter(sex='Male').count()

    bm_f_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Belgian Malinois').filter(capability='EDD').filter(sex='Female').count()
    bm_f_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Belgian Malinois').filter(capability='NDD').filter(sex='Female').count()
    bm_f_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Belgian Malinois').filter(capability='SAR').filter(sex='Female').count()

    #Dutch Sheperd
    ds_m = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Dutch Sheperd').filter(sex='Male').count()
    ds_f = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Dutch Sheperd').filter(sex='Female').count()

    ds_m_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Dutch Sheperd').filter(capability='EDD').filter(sex='Male').count()
    ds_m_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Dutch Sheperd').filter(capability='NDD').filter(sex='Male').count()
    ds_m_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Dutch Sheperd').filter(capability='SAR').filter(sex='Male').count()

    ds_f_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Dutch Sheperd').filter(capability='EDD').filter(sex='Female').count()
    ds_f_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Dutch Sheperd').filter(capability='NDD').filter(sex='Female').count()
    ds_f_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Dutch Sheperd').filter(capability='SAR').filter(sex='Female').count()

    #German Sheperd
    gs_m = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='German Sheperd').filter(sex='Male').count()
    gs_f = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='German Sheperd').filter(sex='Female').count()

    gs_m_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='German Sheperd').filter(capability='EDD').filter(sex='Male').count()
    gs_m_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='German Sheperd').filter(capability='NDD').filter(sex='Male').count()
    gs_m_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='German Sheperd').filter(capability='SAR').filter(sex='Male').count()

    gs_f_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='German Sheperd').filter(capability='EDD').filter(sex='Female').count()
    gs_f_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='German Sheperd').filter(capability='NDD').filter(sex='Female').count()
    gs_f_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='German Sheperd').filter(capability='SAR').filter(sex='Female').count()


    gr_m = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Golden Retriever').filter(sex='Male').count()
    gr_f = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Golden Retriever').filter(sex='Female').count()

    gr_m_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Golden Retriever').filter(capability='EDD').filter(sex='Male').count()
    gr_m_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Golden Retriever').filter(capability='NDD').filter(sex='Male').count()
    gr_m_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Golden Retriever').filter(capability='SAR').filter(sex='Male').count()

    gr_f_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Golden Retriever').filter(capability='EDD').filter(sex='Female').count()
    gr_f_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Golden Retriever').filter(capability='NDD').filter(sex='Female').count()
    gr_f_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Golden Retriever').filter(capability='SAR').filter(sex='Female').count()

    jr_m = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Jack Russel').filter(sex='Male').count()
    jr_f = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Jack Russel').filter(sex='Female').count()

    jr_m_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Jack Russel').filter(capability='EDD').filter(sex='Male').count()
    jr_m_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Jack Russel').filter(capability='NDD').filter(sex='Male').count()
    jr_m_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Jack Russel').filter(capability='SAR').filter(sex='Male').count()

    jr_f_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Jack Russel').filter(capability='EDD').filter(sex='Female').count()
    jr_f_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Jack Russel').filter(capability='NDD').filter(sex='Female').count()
    jr_f_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Jack Russel').filter(capability='SAR').filter(sex='Female').count()

    lr_m = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Labrador Retriever').filter(sex='Male').count()
    lr_f = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Labrador Retriever').filter(sex='Female').count()

    lr_m_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Labrador Retriever').filter(capability='EDD').filter(sex='Male').count()
    lr_m_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Labrador Retriever').filter(capability='NDD').filter(sex='Male').count()
    lr_m_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Labrador Retriever').filter(capability='SAR').filter(sex='Male').count()

    lr_f_edd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Labrador Retriever').filter(capability='EDD').filter(sex='Female').count()
    lr_f_ndd = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Labrador Retriever').filter(capability='NDD').filter(sex='Female').count()
    lr_f_sar = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed='Labrador Retriever').filter(capability='SAR').filter(sex='Female').count()

    bm = bm_m+bm_f
    ds = ds_m+ds_f
    gs = gs_m+gs_f
    gr = gr_m+gr_f
    jr = jr_m+jr_f
    lr = lr_m+lr_f
    t_breed = bm+ds+gs+gr+jr+lr

    edd_f = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(capability='EDD').filter(sex='Female').count()
    ndd_f = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(capability='NDD').filter(sex='Female').count()
    sar_f = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(capability='SAR').filter(sex='Female').count()

    edd_m = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(capability='EDD').filter(sex='Male').count()
    ndd_m = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(capability='NDD').filter(sex='Male').count()
    sar_m = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(capability='SAR').filter(sex='Male').count()

    ndd = ndd_f+ndd_m
    edd = edd_f + edd_m
    sar = sar_f + sar_m

    #finished training data
    ts =[]
    for d in data:
        a = Training_Schedule.objects.filter(k9=d).get(stage='Stage 3.3')
        ts.append(a.date_end.date())


    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'data': data,
        'ts': ts,
        'title': 'Trained K9 List',
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'EDD_count': EDD_count,
        'NDD_count': NDD_count,
        'SAR_count': SAR_count,
        'NDD_demand': NDD_demand,
        'EDD_demand': EDD_demand,
        'SAR_demand': SAR_demand,

        'ndd':ndd,
        'edd':edd,
        'sar':sar,

        'ndd_f':ndd_f,
        'edd_f':edd_f,
        'sar_f':sar_f,

        'ndd_m':ndd_m,
        'edd_m':edd_m,
        'sar_m':sar_m,

        'bm_m':bm_m,
        'bm_f':bm_f,
        'bm_m_edd':bm_m_edd,
        'bm_m_ndd':bm_m_ndd,
        'bm_m_sar':bm_m_sar,
        'bm_f_edd':bm_f_edd,
        'bm_f_ndd':bm_f_ndd,
        'bm_f_sar':bm_f_sar,


        'ds_m':ds_m,
        'ds_f':ds_f,
        'ds_m_edd':ds_m_edd,
        'ds_m_ndd':ds_m_ndd,
        'ds_m_sar':ds_m_sar,
        'ds_f_edd':ds_f_edd,
        'ds_f_ndd':ds_f_ndd,
        'ds_f_sar':ds_f_sar,

        'gs_m':gs_m,
        'gs_f':gs_f,
        'gs_m_edd':gs_m_edd,
        'gs_m_ndd':gs_m_ndd,
        'gs_m_sar':gs_m_sar,
        'gs_f_edd':gs_f_edd,
        'gs_f_ndd':gs_f_ndd,
        'gs_f_sar':gs_f_sar,

        'gr_m':gr_m,
        'gr_f':gr_f,
        'gr_m_edd':gr_m_edd,
        'gr_m_ndd':gr_m_ndd,
        'gr_m_sar':gr_m_sar,
        'gr_f_edd':gr_f_edd,
        'gr_f_ndd':gr_f_ndd,
        'gr_f_sar':gr_f_sar,

        'jr_m':jr_m,
        'jr_f':jr_f,
        'jr_m_edd':jr_m_edd,
        'jr_m_ndd':jr_m_ndd,
        'jr_m_sar':jr_m_sar,
        'jr_f_edd':jr_f_edd,
        'jr_f_ndd':jr_f_ndd,
        'jr_f_sar':jr_f_sar,

        'lr_m':lr_m,
        'lr_f':lr_f,
        'lr_m_edd':lr_m_edd,
        'lr_m_ndd':lr_m_ndd,
        'lr_m_sar':lr_m_sar,
        'lr_f_edd':lr_f_edd,
        'lr_f_ndd':lr_f_ndd,
        'lr_f_sar':lr_f_sar,

        'bm':bm,
        'ds':ds,
        'gs':gs,
        'gr':gr,
        'jr':jr,
        'lr':lr,
        't_breed':t_breed,
    }
    return render (request, 'unitmanagement/trained_list.html', context)

def classified_list(request):
    data = K9.objects.filter(training_status="Classified").filter(status="Material Dog")

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'data': data,
        'title': 'Classified K9 List',
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/classified_list.html', context)
#
# def change_equipment(request, id):
#     data = Requests.objects.get(id=id)
#     style = ""
#     changedate = dt.datetime.now()
#
#     if request.method == 'POST':
#         if 'ok' in request.POST:
#             data.request_status = "Approved"
#             data.date_approved = changedate
#             data.save()
#             #subtract inventory
#             equipment = Miscellaneous.objects.get(miscellaneous=data.equipment)
#             if equipment.quantity > 0:
#                 equipment.quantity = equipment.quantity-1
#                 equipment.save()
#
#                 Miscellaneous_Subtracted_Trail.objects.create(inventory=equipment, user=user_session(request),
#                                                          quantity=1,
#                                                          date_subtracted=dt.date.today(),
#                                                          time=dt.datetime.now())
#                 style = "ui green message"
#                 messages.success(request, 'Equipment Approved!')
#
#             else:
#                 style = "ui red message"
#                 messages.success(request, 'Insufficient Inventory!')
#
#         else:
#             data.request_status = "Denied"
#             data.date_approved = changedate
#             data.save()
#             style = "ui green message"
#             messages.success(request, 'Equipment Denied!')
#
#     #NOTIF SHOW
#     notif_data = notif(request)
#     count = notif_data.filter(viewed=False).count()
#     user = user_session(request)
#     context = {
#         'data': data,
#         'style': style,
#         'notif_data':notif_data,
#         'count':count,
#         'user':user,
#     }
#
#     return render (request, 'unitmanagement/change_equipment.html', context)

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
    user = user_session(request)
    style='ui green message'
    if user.position == 'Team Leader':
        ta = Team_Assignment.objects.get(team_leader=user)

        tdd = Team_Dog_Deployed.objects.filter(team_assignment=ta).filter(status='Deployed')

        k9 = []
        for td in tdd:
            k9.append(td.k9)
        data = K9_Incident.objects.filter(k9__in=k9).filter(status='Pending').exclude(incident='Sick').exclude(incident='Accident')

    elif user.position == 'Veterinarian':
        data = K9_Incident.objects.filter(status='Pending').filter(incident='Accident')
    else:
        data = K9_Incident.objects.filter(status='Pending').exclude(incident='Sick').exclude(incident='Accident')


    if request.method == "POST":
        i = request.POST.get('input_id')
        dc = request.POST.get('death_cert')
        date = request.POST.get('date_died')
        ki = K9_Incident.objects.get(id=i)

        k9 = K9.objects.get(id=ki.k9.id)
        k9.status= 'Dead'
        k9.training_status = 'Dead'
        k9.death_cert = dc
        k9.death_date = date

        ki.status = 'Done'
        ki.save()
        k9.save()
        messages.success(request, 'K9 Died...')
        return redirect('unitmanagement:k9_incident_list')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'title': "K9 Incident List",
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data':data,
    }
    return render (request, 'unitmanagement/k9_incident_list.html', context)

def follow_up(request, id):
    data = Health.objects.get(id=id)
    i = K9_Incident.objects.get(id=data.incident_id.id)
    medicine = HealthMedicine.objects.filter(health=data)
    dog = K9.objects.get(id = data.dog.id)

    th = Transaction_Health.objects.create(health=data, incident=i)
    data.follow_up = True
    data.save()

    request.session['health'] = th.id

    return redirect('unitmanagement:k9_sick_form')

def k9_sick_form(request):
    user = user_session(request)
    form = K9IncidentForm(request.POST or None, request.FILES or None)
    style='ui green message'
    form2 = DateForm(request.POST or None)
    handler = K9.objects.filter(handler=user)
    form.fields['k9'].queryset =  handler
    health = None
    h = None

    if 'health' in request.session:
        h = request.session['health']

    try:
        th = Transaction_Health.objects.filter(status='Pending').get(id=h)
        health = Health.objects.get(id=th.health.id)
    except ObjectDoesNotExist:
        th =  None


    if request.method == "POST":
        if form.is_valid():

            form = form.save(commit=False)
            form.incident = 'Sick'
            form.reported_by = user
            form.k9.status = form.incident
            form.save()

            files = request.FILES.getlist('image_file')

            #Images
            for f in files:
                Image.objects.create(incident_id=form, image=f)

            #Follow up Handler side
            if th != None:
                th.follow_up = form
                th.health.follow_up_done=True
                th.save()

            if health != None:
                health.follow_up = True
                health.save()

            #what happens to the previous health if nag follow-up and handler?

            style = "ui green message"
            messages.success(request, 'Health Concern has been successfully Reported!')

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
        'form2':form2,
        'health':health,
    }
    return render (request, 'unitmanagement/k9_sick_form.html', context)

def k9_retreived(request, id):
    data = K9_Incident.objects.get(id=id)
    data.status = 'Done'
    data.k9.status = 'Working Dog'
    data.save()
    messages.success(request, 'K9 retrieval has been confirmed and data has been updated!')
    return redirect('unitmanagement:k9_incident_list')

def k9_accident(request, id):
    accident = request.GET.get('accident')
    data = K9_Incident.objects.get(id=id)
    data.status = 'Done'
    data.save()

    k9 = K9.objects.get(id=data.k9.id)

    if accident == 'recovered':
        k9.status = 'Working Dog'
        messages.success(request, 'K9 has recovered!')
    else:
        k9.status = 'Died'
        k9.training_status = 'Died'
        messages.success(request, 'K9 died..')

    k9.save()
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
        d =  (da.date_done - date)
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

            if f.incident == 'Died':
                user.status = 'Died'
                user.partnered = False
                user.assigned = False
                b.handler = None
            elif f.incident == 'MIA':
                user.status = 'MIA'
                user.partnered = False
                user.assigned = False
                b.handler = None
                #if MIA, kasama ba ang aso?

            user.save()
            b.save()
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

def reassign_assets(request, id):
    form = assign_handler_form(request.POST or None)
    style = ""
    k9 = K9.objects.get(id=id)

    handler = User.objects.filter(status='Working').filter(position='Handler').filter(partnered=False)

    g = []
    for h in handler:

        if k9.capability == 'NDD':
            cap = Handler_K9_History.objects.filter(handler=h).filter(k9__capability=k9.capability).count()
        elif k9.capability == 'EDD':
            cap = Handler_K9_History.objects.filter(handler=h).filter(k9__capability=k9.capability).count()
        else:
            cap = Handler_K9_History.objects.filter(handler=h).filter(k9__capability=k9.capability).count()

        s=[cap]
        g.append(s)

    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            f = form.save(commit=False)
            f.k9 = k9
            f.save()

            #Handler Update
            h = User.objects.get(id= f.handler.id)
            h.partnered = True
            h.save()

            #K9 Update
            k = K9.objects.get(id=f.k9.id)
            k.handler=h
            k.save()

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
        'Title': "Available Handlers for " + k9.name,
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'k9':k9,
        'g':g,
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

# TODO 
# Due Retired
def due_retired_list(request):
    style='ui green message'
    cb = Call_Back_K9.objects.filter(status='Pending')

    cb_list = []
    for c in cb:
        cb_list.append(c.k9.id)
         
    data = K9.objects.filter(status='Due-For-Retirement').exclude(training_status='For-Adoption').exclude(training_status='Adopted').exclude(training_status='Light Duty').exclude(training_status='Retired').exclude(training_status='Dead').exclude(assignment=None).exclude(id__in=cb_list) 

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Due for Retirement List",
        'data': data,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/due_retired_list.html', context)

def due_retired_call(request, id):
    k9 = K9.objects.get(id=id)
    cb = Call_Back_K9.objects.create(k9=k9)
    Notification.objects.create(k9=k9,user=k9.handler,other_id=cb.id,notif_type='call_back', position='Handler', message=str(k9) + ' is due for retirement. Please return to PCGK9-Taguig Base.')
    
    messages.success(request, 'You have called ' + str(k9) + ' back to base.')
    return redirect ('unitmanagement:due_retired_list')

def confirm_base_arrival(request):
    dd = Call_Back_K9.objects.all()

    data = []
    for d in dd:
        handler = User.objects.get(id=d.k9.handler.id)
        a = [d,handler]
        data.append(a)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title': "Called Back to Base List - Confirm Arrival",
        'data': data,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/confirm_base_arrival.html', context)

def confirm_arrive(request,id):
    cb = Call_Back_K9.objects.get(id=id)
    #k9
    k9 = K9.objects.get(id=cb.k9.id)
    k9.training_status = 'Light Duty'
    k9.status = 'Working Dog'
    k9.assignment = None
    k9.handler = None

    #handler
    handler = Handler.objects.get(id=k9.handler.id)
    handler.partnered = False
    handler.assigned = False

    k9.save()
    handler.save()

    messages.success(request, 'You have confirmed the arrival of ' + str(cb.k9.handler) + ' and ' +str(cb.k9) + ' back to base.')
    cb.delete()
    return redirect ('unitmanagement:confirm_base_arrival')

def confirm_going_back(request,id):
    cb = Call_Back_K9.objects.get(id=id)
    cb.status='Confirmed'
    cb.save()
    return redirect ('profiles:handler_dashboard')

# TODO 
# transfer request list
def transfer_request_list(request):
    # for sched in schedules:
    #     if (sched.date_start >= data2.start_date and sched.date_start <= data2.end_date) or (sched.date_end >= data2.start_date and sched.date_end <= data2.end_date) or (data2.start_date >= sched.date_start and data2.start_date <= sched.date_end) or (data2.end_date >= sched.date_start and data2.end_date <= sched.date_end):
    #         deployable = 0

    style='ui green message'
    rt =  Request_Transfer.objects.filter(status='Pending')

    data = []

    for d in rt:
        count = Request_Transfer.objects.filter(status='Pending').filter(location_to=d.location_to).exclude(id=d.id).count()
        a = [d, count]
        data.append(a)

    #Code here for approval of transfer
    if request.method == 'POST':
        date = request.POST.get('date_input')
        match_id = request.POST.get('select')
        requester_id = request.POST.get('requester')
        
        match = User.objects.get(id=match_id)
        requester = User.objects.get(id=requester_id)

        if 'approve' in request.POST:
            print('yes',date, match, requester)
        else:
            print('no',date, match, requester)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {
        'title': "Transfer Request List",
        'data': data,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render (request, 'unitmanagement/transfer_request.html', context)

def transfer_request_form(request):
    user = user_session(request)
    form = RequestTransferForm(request.POST or None)
    k9 = K9.objects.get(handler=user)
    schedules = K9_Schedule.objects.filter(k9 = k9)

    td = None
    loc = None
    try:
        td = Team_Dog_Deployed.objects.filter(k9=k9).filter(date_pulled=None).exclude(team_requested = None).latest('date_added')

        loc = Team_Assignment.objects.get(id=td.team_requested.id)
        form.initial['handler'] = User.objects.get(id=user.id)
        form.initial['location_from'] = loc
        form.fields['location_to'].queryset = Team_Assignment.objects.exclude(id=loc.id)
    except: pass
    style='ui green message'

    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            f = form.save(commit=False)
            f.location_from = loc
            f.handler = user
            f.save(commit = False)

            date_of_transfer = f.date_of_transfer
            today = datetime.today().date()
            deploy = True
            for sched in schedules:
                if date_of_transfer >= sched.date_start and date_of_transfer <= sched.date_end:
                    deploy = False

                delta = date_of_transfer - td.date_added
                if delta.days >= 730:
                    deploy = False

            if deploy == True:
                style='ui green message'
                messages.success(request,'You have submitted a transfer request!')
            
                return redirect('unitmanagement:transfer_request_form')
            else:
                style = 'ui red message'
                messages.success(request, 'Date input has conflict with a request scheduled!')
        else:
            style='ui red message'
            messages.success(request,'Invalid Input!')
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()

    context = {
        'title': "Transfer Request Form",
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'form':form,
        'events' : schedules
    }
    return render (request, 'unitmanagement/transfer_request_form.html', context)

def replenishment_form(request):
    user = user_session(request)
    style = 'ui green message'
    form = ReplenishmentForm(request.POST or None)

    food_formset = inlineformset_factory(Replenishment_Request, Food_Request, form=RequestFood, extra=1, can_delete=True)

    med_formset = inlineformset_factory(Replenishment_Request, Medicine_Request, form=RequestMedicine, extra=1, can_delete=True)
    
    misc_formset = inlineformset_factory(Replenishment_Request, Miscellaneous_Request,form=RequestMiscellaneous, extra=1, can_delete=True)

    form.fields['handler'].queryset = User.objects.filter(id=user.id)

    formset1 = food_formset(request.POST or None, prefix='food')
    formset2 = med_formset(request.POST or None, prefix='med')
    formset3 = misc_formset(request.POST or None, prefix='misc')

    # form
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            f=form.save()

            if formset1.is_valid() and formset2.is_valid() and formset3.is_valid():
                for form in formset1:   
                    form = form.save(commit=False)
                    form.request = f
                    # form.save()
                    print(form)

          
                for form in formset2:
                    form = form.save(commit=False)
                    form.request = f
                    # form.save()
                    print(form)

           
                for form in formset3:
                    form = form.save(commit=False)
                    form.request = f
                    # form.save()
                    print(form)
            else:
                message.warning(request, 'Invalid Input')
         
            return redirect('unitmanagement:replenishment_form')
            # return redirect('profiles:handler_dashboard')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {
        'title': "Item Replenishment Request Form",
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'form':form,
        'med_formset':med_formset(),
        'food_formset':food_formset(),
        'misc_formset':misc_formset(),
    }
    return render (request, 'unitmanagement/replenishment_form.html', context)

def replenishment_confirm(request):
    user = user_session(request)
    style = 'ui green message'

    d1 = Replenishment_Request.objects.filter(status='Pending')
    d2 = Replenishment_Request.objects.filter(status='Confirmed')

    data1 = []
    for d in d1:
        ta1 = Team_Assignment.objects.get(team_leader=d.handler)
        a = [d,ta1]
        data1.append(a)

    data2 = []
    for d in d2:
        ta1 = Team_Assignment.objects.get(team_leader=d.handler)
        a = [d,ta1]
        data2.append(a)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()

    context = {
        'title': "Item Replenishment Requests",
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data1':data1,
        'data2':data2,
    }
    return render (request, 'unitmanagement/replenishment_request_confirm.html', context)

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

        if k9.capability == 'NDD':
            cap = Training_History.objects.filter(handler=h).filter(k9__capability='NDD').filter(k9__trained='Trained').count()
            cap_f = Training_History.objects.filter(handler=h).filter(k9__capability='NDD').filter(k9__trained='Failed').count()
        elif k9.capability == 'EDD':
            cap = Training_History.objects.filter(handler=h).filter(k9__capability='EDD').filter(k9__trained='Trained').count()
            cap_f = Training_History.objects.filter(handler=h).filter(k9__capability='EDD').filter(k9__trained='Failed').count()
        else:
            cap = Training_History.objects.filter(handler=h).filter(k9__capability='SAR').filter(k9__trained='Trained').count()
            cap_f = Training_History.objects.filter(handler=h).filter(k9__capability='SAR').filter(k9__trained='Failed').count()

        c = 0
        f = 0
        ct = cap+cap_f
        if cap != 0:
            c = int((cap / ct) * 100)

        s = [cap,ct,c]
        g.append(s)
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
            return redirect('unitmanagement:classified_list')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {
        'Title': "Available Handlers for " + k9.name,
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
# K9 Died
def confirm_death(request, id):
    i = K9_Incident.objects.get(id=id)
    i.status = 'Done'
    i.save()

    k9 = K9.objects.get(id=i.k9.id)
    k9.status = "Dead"
    k9.training_status = "Dead"
    k9.save()

    messages.success(request, i.k9.name + 'has been confirmed dead...')

    return redirect('unitmanagement:k9_incident_list')

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

    t = Transaction_Health.objects.filter(incident__status='Pending').exclude(health__follow_up=True)
    a = []
    for t in t:
        t.append(t.incident.id)


    data =K9_Incident.objects.filter(incident='Sick').filter(status='Pending')
    data2 = K9_Incident.objects.filter(incident='Sick').filter(status='Done')

    d = Transaction_Health.objects.filter(incident__status='Pending').filter(health__follow_up=True).exclude(health__follow_up_done=True)
    f = []

    for d in d:
        f.append(d.health.id)

    th = Health.objects.filter(follow_up_date__gte=dt.date.today()).exclude(follow_up_done=True)

    print(th)

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
        'th':th,
    }
    return render (request, 'unitmanagement/k9_sick_list.html', context)

#TODO
#sick list
def k9_sick_details(request, id):

    data = K9_Incident.objects.get(id=id)

    health_id = Health.objects.filter(dog=data.k9)
    image = Image.objects.filter(incident_id=data)
    medicine_formset = inlineformset_factory(Health, HealthMedicine, form=HealthMedicineForm, extra=1, can_delete=True)
    style=""

    th = None
    h = None
    hh = None
    try:
        th = Transaction_Health.objects.filter(status='Pending').get(incident=data)
        hh = Health.objects.filter(id=th.health.id).latest('id')
        h = HealthMedicine.objects.filter(health=hh)
    except ObjectDoesNotExist:
        try:
            th = Transaction_Health.objects.filter(status='Pending').get(follow_up=data)
            if (th != None):
                hh = Health.objects.filter(id=th.health.id).latest('id')
                h = HealthMedicine.objects.filter(health=hh)
            else:
                th = None
                h = None
                hh = None
        except ObjectDoesNotExist:
            th = None
            h = None
            hh = None


    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)

    form = HealthForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            health = form.save(commit=False)
            health.dog = data.k9
            health.incident_id = data
            health.veterinary = user_in_session
            health.save()
            new_form = health.pk
            form_instance = Health.objects.get(id=new_form)
            dog = K9.objects.get(id=health.dog.id)

            # transaction health
            if th != None:
                th.status = 'Done'
                th.health = health
                th.save()

                hh.follow_up_done = True
                hh.save()

            if health.follow_up == True:
                Transaction_Health.objects.create(health=health, incident=data)

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
                        med.quantity = med.quantity - f.quantity
                        med.save()
                        Medicine_Subtracted_Trail.objects.create(inventory = med, user=user_in_session, quantity = f.quantity)

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
        'th':th,
        'h':h,
        'health_id':health_id,
    }
    return render (request, 'unitmanagement/k9_sick_details.html', context)


class TeamLeaderView(APIView):
    def get(self, request, format=None):
        user = user_session(request)
        ta = Team_Assignment.objects.get(team_leader=user)
        tdd = Team_Dog_Deployed.objects.filter(team_assignment=ta).filter(status='Deployed')

        # Incident
        er = Incidents.objects.filter(location = ta.location).filter(type='Explosives Related').count()
        nr = Incidents.objects.filter(location = ta.location).filter(type='Narcotics Related').count()
        sarr = Incidents.objects.filter(location = ta.location).filter(type='Search and Rescue Related').count()
        otr = Incidents.objects.filter(location = ta.location).filter(type='Others').count()

        labels= ['Explosive','Narcotics', 'Search and Rescue', 'Others']
        default_items = [er, nr, sarr, otr]

        # K9 Demand and Supply
        d_edd = ta.EDD_demand
        d_ndd = ta.NDD_demand
        d_sar = ta.SAR_demand

        s_edd = ta.EDD_deployed
        s_ndd = ta.NDD_deployed
        s_sar = ta.SAR_deployed


        demand_items = [d_edd, d_ndd, d_sar]
        supply_items = [s_edd, s_ndd, s_sar]

        # Perfromance

        tdd = Team_Dog_Deployed.objects.filter(team_assignment=ta).filter(status='Deployed')

        k9_id = []

        for td in tdd:
            k9_id.append(td.k9.id)

        k9 = K9.objects.filter(id__in=k9_id)

        k9_perf = []

        #get all k9s
        for k in k9:

            jan = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=1).aggregate(avg=Avg('rating'))['avg']
            feb = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=2).aggregate(avg=Avg('rating'))['avg']
            mar = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=3).aggregate(avg=Avg('rating'))['avg']
            apr = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=4).aggregate(avg=Avg('rating'))['avg']
            may = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=5).aggregate(avg=Avg('rating'))['avg']
            jun = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=6).aggregate(avg=Avg('rating'))['avg']
            jul = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=7).aggregate(avg=Avg('rating'))['avg']
            aug = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=8).aggregate(avg=Avg('rating'))['avg']
            sep = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=9).aggregate(avg=Avg('rating'))['avg']
            oct = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=10).aggregate(avg=Avg('rating'))['avg']
            nov = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=11).aggregate(avg=Avg('rating'))['avg']
            dec = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=12).aggregate(avg=Avg('rating'))['avg']

            if jan == None:
                jan = 0
            if feb == None:
                feb = 0
            if mar == None:
                mar = 0
            if apr == None:
                apr = 0
            if may == None:
                may = 0
            if jun == None:
                jun = 0
            if jul == None:
                jul = 0
            if aug == None:
                aug = 0
            if sep == None:
                sep = 0
            if oct == None:
                oct = 0
            if nov == None:
                nov = 0
            if dec == None:
                dec = 0


            perf_items = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
            k9_perf.append(perf_items)

        fou = []

        for td in tdd:
            fou.append(str(td.k9.name) + ' - ' + str(td.handler.lastname))

        data = {
            "labels":labels,
            "default":default_items,
            "demand":demand_items,
            "supply":supply_items,
            "performance":k9_perf,
            "fou":fou,
        }
        return Response(data)

class HandlerView(APIView):
    def get(self, request, format=None):
        user = user_session(request)
        sched_items = []
        today = date.today()
        k9=None
        try:
            k9 = K9.objects.get(handler=user)
            jan = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=1).aggregate(avg=Avg('rating'))['avg']
            feb = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=2).aggregate(avg=Avg('rating'))['avg']
            mar = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=3).aggregate(avg=Avg('rating'))['avg']
            apr = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=4).aggregate(avg=Avg('rating'))['avg']
            may = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=5).aggregate(avg=Avg('rating'))['avg']
            jun = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=6).aggregate(avg=Avg('rating'))['avg']
            jul = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=7).aggregate(avg=Avg('rating'))['avg']
            aug = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=8).aggregate(avg=Avg('rating'))['avg']
            sep = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=9).aggregate(avg=Avg('rating'))['avg']
            oct = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=10).aggregate(avg=Avg('rating'))['avg']
            nov = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=11).aggregate(avg=Avg('rating'))['avg']
            dec = Daily_Refresher.objects.filter(k9=k).filter(date__year=datetime.now().year).filter(date__month=12).aggregate(avg=Avg('rating'))['avg']

        except:
            jan=0
            feb=0
            mar=0
            apr=0
            may=0
            jun=0
            jul=0
            aug=0
            sep=0
            oct=0
            nov=0
            dec=0

        if k9 != None:
            sched = K9_Schedule.objects.filter(k9=k9).filter(date_end__gte=today)

            for items in sched:
                i = [items.dog_request.location,items.dog_request.event_name,items.dog_request.total_dogs_demand,items.dog_request.total_dogs_deployed, items.date_start, items.date_end]
                sched_items.append(i)

        perf_items = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]

        data = {
            "performance":perf_items,
            "sched":sched_items,
        }
        return Response(data)

class VetView(APIView):
    def get(self, request, format=None):
        user = user_session(request)
        # In heat K9 per Month
        jan = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=1).count()
        feb = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=2).count()
        mar = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=3).count()
        apr = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=4).count()
        may = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=5).count()
        jun = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=6).count()
        jul = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=7).count()
        aug = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=8).count()
        sep = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=9).count()
        oct = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=10).count()
        nov = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=11).count()
        dec = K9.objects.filter(sex='Female').filter(last_proestrus_date__month=11).count()

        if jan == None:
            jan = 0
        if feb == None:
            feb = 0
        if mar == None:
            mar = 0
        if apr == None:
            apr = 0
        if may == None:
            may = 0
        if jun == None:
            jun = 0
        if jul == None:
            jul = 0
        if aug == None:
            aug = 0
        if sep == None:
            sep = 0
        if oct == None:
            oct = 0
        if nov == None:
            nov = 0
        if dec == None:
            dec = 0


        in_heat_items = [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]

        data = {
            "in_heat":in_heat_items,
        }
        return Response(data)

class CommanderView(APIView):
    def get(self, request, format=None):
        user = user_session(request)
        area = Area.objects.filter(commander=user)
        location = Location.objects.filter(area__in = area)

        team = Team_Assignment.objects.filter(location__in =location)
        team_items = []
        for t in team:
            pass

        data = {
            "team_items":team_items,
        }
        return Response(data)

class TrainerView(APIView):
    def get(self, request, format=None):
        user = user_session(request)

        NDD_count = K9.objects.filter(capability='NDD').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()
        EDD_count = K9.objects.filter(capability='EDD').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()
        SAR_count = K9.objects.filter(capability='SAR').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()


        NDD_demand = list(Team_Assignment.objects.aggregate(Sum('NDD_demand')).values())[0]
        EDD_demand = list(Team_Assignment.objects.aggregate(Sum('EDD_demand')).values())[0]
        SAR_demand = list(Team_Assignment.objects.aggregate(Sum('SAR_demand')).values())[0]


        current = [NDD_count,EDD_count,SAR_count]
        demand = [NDD_demand,EDD_demand,SAR_demand]

        ndd_train = K9.objects.filter(capability='NDD').filter(training_status='On-Training').count()
        edd_train = K9.objects.filter(capability='EDD').filter(training_status='On-Training').count()
        sar_train = K9.objects.filter(capability='SAR').filter(training_status='On-Training').count()

        pie_data = [ndd_train,edd_train,sar_train]
        data = {
            "current":current,
            "demand":demand,
            "pie_data":pie_data,
        }
        return Response(data)


def load_handler(request):

    handler = None
    pi = None
    edd = None
    ndd = None
    sar = None
    type_text = None
    k9 = None
    cc_ac = 0
    cc_in = 0
    requester = None
    try:
        handler_id = request.GET.get('handler')
        type_text = request.GET.get('type_text')
        requester = request.GET.get('requester')
        handler = User.objects.get(id=handler_id)
        k9 = K9.objects.get(handler=handler)
        
        pi = Personal_Info.objects.get(UserID=handler)
        edd = Handler_K9_History.objects.filter(handler=handler).filter(k9__capability='EDD').count()
        ndd = Handler_K9_History.objects.filter(handler=handler).filter(k9__capability='NDD').count()
        sar = Handler_K9_History.objects.filter(handler=handler).filter(k9__capability='SAR').count()
        
        cc_ac = Handler_Incident.objects.filter(handler=handler).filter(incident='Rescued People').filter(incident='Made an Arrest').count()
        cc_in = Handler_Incident.objects.filter(handler=handler).filter(incident='Poor Performance').filter(incident='Violation').count()
    except:
        pass

    context = {
        'handler': handler,
        'requester':requester,
        'pi':pi,
        'ndd':ndd,
        'edd':edd,
        'sar':sar,
        'k9':k9,
        'cc_ac':cc_ac,
        'cc_in':cc_in,
        'type_text':type_text,
    }

    return render(request, 'unitmanagement/handler_data.html', context)

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

def load_transfer(request):

    #TODO 3 day gap between two handlers
    transfer = None
    k9 = None
    matches = None
    c_ac = None
    c_in = None
    incident = None
    try:
        transfer_id = request.GET.get('id')
        transfer = Request_Transfer.objects.get(id=transfer_id)
        k9= K9.objects.get(handler=transfer.handler)
        personal = Personal_Info.objects.get(UserID = transfer.handler)

        matches = Request_Transfer.objects.filter(location_to=transfer.location_from)
        matches_within_three = []
        for match in matches:
            match_date_of_transfer = match.date_of_transfer
            delta = match_date_of_transfer - transfer.date_of_transfer
            if abs(delta.days) <= 3:
               matches_within_three.append(match.id)

        matches = matches.exclude(id__in = matches_within_three)

        incident = Handler_Incident.objects.filter(handler=transfer.handler)
        c_ac = Handler_Incident.objects.filter(handler=transfer.handler).filter(incident='Rescued People').filter(incident='Made an Arrest').count()
        c_in = Handler_Incident.objects.filter(handler=transfer.handler).filter(incident='Poor Performance').filter(incident='Violation').count()
        
    except:
        pass

    context = {
        'transfer': transfer,
        'k9': k9,
        'matches':matches,
        'incident':incident,
        'c_ac':c_ac,
        'c_in':c_in,
        'personal' : personal
    }

    return render(request, 'unitmanagement/transfer_data.html', context)

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

def load_health(request):

    health = None
    h = None
    try:
        health_id = request.GET.get('health')
        health = Health.objects.get(id=health_id)

        h = HealthMedicine.objects.filter(health=health)

    except:
        pass

    context = {
        'health': health,
        'h': h,
    }

    return render(request, 'unitmanagement/health_data.html', context)

def load_image(request):

    image = None
    try:
        image_id = request.GET.get('image')
        image = Image.objects.get(id=image_id)
    except:
        pass
    context = {
        'image': image,
    }

    return render(request, 'unitmanagement/image_data.html', context)


def load_incident(request):

    data_load = None
    try:
        id = request.GET.get('id')
        data_load = K9_Incident.objects.get(id=id)
    except:
        pass

    context = {
        'data_load': data_load,
    }

    return render(request, 'unitmanagement/incident_data.html', context)

def load_yearly_vac(request):

    data = None
    form = None
    type = None
    initial = None
    disease = None
    try:
        id = request.GET.get('id')
        type = request.GET.get('type')
        initial = request.GET.get('intial')
        disease = request.GET.get('disease')

        data = K9.objects.get(id=id)
        form = VaccinationUsedForm(request.POST or None)

        if type == 'Deworming':
            form.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Deworming').exclude(quantity=0)
        elif type == 'DHPP':
            form.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='DHPPiL4').exclude(quantity=0)
        elif type == 'Anti-Rabies':
            form.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Anti-Rabies').exclude(quantity=0)
        elif type == 'Bordertella':
            form.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Bordetella Bronchiseptica Bacterin').exclude(quantity=0)
        elif type == 'DHPPIL4':
            form.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='DHPPIL4').exclude(quantity=0)
        elif type == 'Heartworm':
            form.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Heartworm').exclude(quantity=0)
        elif type == 'TickFlee':
            form.fields['vaccine'].queryset = Medicine_Inventory.objects.filter(medicine__immunization='Tick and Flea').exclude(quantity=0)
    except:
        pass

    context = {
        'data': data,
        'form': form,
        'type':type,
        'initial':initial,
        'disease':disease,
    }

    return render(request, 'unitmanagement/yearly_vac_data.html', context)

def load_physical(request):

    form = None
    score = None
    try:
        id = request.GET.get('id')
        type = request.GET.get('type')

        if type == 'details':
            phex = PhysicalExam.objects.filter(dog=id).latest('date')
            form = PhysicalExamForm(request.POST or None, instance=phex)
            score = phex.body_score
        else:
            form = PhysicalExamForm(request.POST or None)
            form.fields['dog'].initial = K9.objects.get(id=id)
            form.fields['dog'].queryset = K9.objects.filter(id=id)

    except:
        pass

    context = {
        'form': form,
        'score': score,
    }

    return render(request, 'unitmanagement/physical_data.html', context)

def load_k9_data(request):

    k9 = None
    remarks = None
    h_count = None
    health = None
    train = None

    try:
        k9_id = request.GET.get('id')
        k9 = K9.objects.get(id=k9_id)
        remarks = Training_Schedule.objects.filter(k9=k9).exclude(stage = "Stage 0")
        h_count = Health.objects.filter(dog=k9).count()
        health = Health.objects.filter(dog=k9)
        train = Training.objects.filter(k9=k9).get(training=k9.capability)

        female = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed=k9.breed).filter(capability=k9.capability).filter(sex='Female').count()

        male = K9.objects.filter(Q(training_status='For-Breeding')|Q(training_status='Breeding')).filter(breed=k9.breed).filter(capability=k9.capability).filter(sex='Male').count()
    except: pass

    print("TRAIN")
    print(train)

    context = {
        'k9': k9,
        'remarks': remarks,
        'h_count': h_count,
        'health': health,
        'train': train,
        'female': female,
        'male': male,
    }

    return render(request, 'unitmanagement/k9_data_trained.html', context)

def k9_checkup_pending(request):
    removal = TempCheckup.objects.all()

    style = ""
    #TODO Save schedule before deletion
    if request.method == "POST":
        for item in removal:
            sched = K9_Schedule.objects.create(k9 = item.k9, status = "Checkup", date_start = item.date)
            sched.save()
            style = "ui green message"
            messages.success(request, 'You have scheduled ' + str(item.k9) + ' for checkup on ' + str(item.date) + "!")

    removal.delete()

    # TODO remove all checkups missed ./
    # TODO remove checkups pag valid ba yung latest checkup
    # TODO remove if missed na yung deployment date

    current_appointments = K9_Schedule.objects.filter(status = "Checkup").exclude(date_start__lt=datetime.today().date())

    k9s_exclude = []

    for item in current_appointments:
            k9s_exclude.append(item.k9)

    pending_schedule = K9_Schedule.objects.filter(status = "Initial Deployment").exclude(k9__in = k9s_exclude).exclude(date_start__lt=datetime.today().date())
    date_form = DateForm()

    k9s_exclude2 = []
    for item in pending_schedule:
        delta = datetime.today().date() - item.date_start

        print(item.k9)
        print(str(datetime.today().date()) + " - " + str(item.date_start) + " = " + str(delta.days))

        phex = False
        try:
            checkup = PhysicalExam.objects.filter(dog=item.k9).latest('id')
            delta2 = datetime.today().date() - checkup.date
            if checkup.cleared == True and delta2.days <= 90:  # also checks if last checkup is within 3 months
                phex = True #Pag true, wag na isama sa checkup list kasi valid pa
        except:
            pass

        if delta.days > 0 and phex == False:  # Nalagapasan na checkup date
            k9s_exclude2.append(item.k9)

    pending_schedule = pending_schedule.exclude(k9__in = k9s_exclude2)

    context = {
        'k9_pending': pending_schedule,
        'events' : current_appointments,
        'date_form': date_form['date'].as_widget(),
        'selected_list': [],
        'style' : style
    }

    return render(request, 'unitmanagement/k9_checkup_pending.html', context)

def load_appointments(request):

    appointments = None
    date = None
    try:
        date = request.GET.get('date')
        print("PRINT DATE")
        print(date)
        new_date = parse(date)
        print(new_date)
        appointments = K9_Schedule.objects.filter(status="Checkup", date_start=new_date)
    except:
        pass


    context = {
        'appointments': appointments,
        'new_date': str(date),
    }

    return render(request, 'unitmanagement/ajax_load_appointments.html', context)


#TODO Hide items from available units when they are already scheduled
def load_checkups(request):
    fullstring = request.GET.get('fullstring')
    fullstring = json.loads(fullstring)

    k9_list = []
    k9_list_id = []

    try:
        date = request.GET.get('date')
        print("DATE")
        print(date)
        date = parse(date)

        for item in fullstring.values():
            k9 = K9.objects.get(id=item)
            k9_list.append(k9)
            k9_list_id.append(k9.id)

            deployment = K9_Schedule.objects.filter(k9 = k9, status = "Initial Deployment").order_by('-id')[0]

            # >>>>>>>

            if TempCheckup.objects.filter(k9=k9).exists():
                pass
            else:
                temp = TempCheckup.objects.create(date=date, k9=k9, deployment_date = deployment.date_start)
                temp.save()

                removal = TempCheckup.objects.exclude(id=temp.id).filter(k9=k9).filter(
                    date=date)  # This line removes duplicates
                removal.delete()

    except:
        for item in fullstring.values():
            k9 = K9.objects.get(id=item)
            k9_list.append(k9)
            k9_list_id.append(k9.id)

            # >>>>>>>

            if TempCheckup.objects.filter(k9=k9).exists():
                pass
            else:
                removal = TempCheckup.objects.filter(k9=k9)  # Dapat icheck niya kung ano yung mga hindi naka select
                removal.delete()

    # pending_schedule = K9_Schedule.objects.filter(status="Initial Deployment").exclude(k9__in = k9_list)

    removal = TempCheckup.objects.exclude(k9__in=k9_list)
    removal.delete()


    temp = TempCheckup.objects.all()


    context = {
        'checkups' : temp,
        'selected_list': k9_list_id,

    }

    return render(request, 'unitmanagement/ajax_load_checkups.html', context)

def load_item_food(request):
    fd = None
    try:
        food_id = request.GET.get('id')
        fd = Food.objects.get(id=food_id)
    except:
        pass

    data = {
        'food':fd.id,
        'unit':fd.unit,
    }
    return JsonResponse(data)

def load_item_med(request):
    med = None
    try:
        med_id = request.GET.get('id')
        med = Medicine_Inventory.objects.get(id=med_id)
    except:
        pass

    data = {
        'med':med.id,
        'unit':'pc',
    }
    return JsonResponse(data)

def load_item_misc(request):
    misc = None
    try:
        misc_id = request.GET.get('id')
        misc = Miscellaneous.objects.get(id=misc_id)
    except:
        pass

    data = {
        'misc':misc.id,
        'unit':misc.uom,
    }
    return JsonResponse(data)

def current_team(K9):
    team_dog_deployed = Team_Dog_Deployed.objects.filter(k9=K9).latest('id')
    team_assignment = None

    if (team_dog_deployed.date_pulled is not None):
        team_assignment_id = team_dog_deployed.team_assignment.id
        team_assignment = Team_Assignment.objects.get(id=team_assignment_id)

    return team_assignment


def k9_checkup_list_today(request):

    #TODO Highlight rows if today
    checkups = K9_Schedule.objects.filter(status = "Checkup").exclude(date_start__lt=datetime.today().date())

    k9_list = []
    for sched in checkups:
        k9_list.append(sched.k9)

    #TODO show k9 if there are no valid checkups

    k9_exclude_list = [] #Does not need to be checkuped
    for k9 in k9_list:
        try:
            checkup = PhysicalExam.objects.filter(dog=k9).latest('id')  # TODO Also check if validity is worth 3 months
            delta = datetime.today().date() - checkup.date
            if checkup.cleared == True and delta.days <= 90: #3 months
                k9_exclude_list.append(k9)
                print(checkup.cleared)
                print(delta.days)
        except: pass

    checkups = checkups.exclude(k9__in = k9_exclude_list)

    checkup_list = []
    for checkup in checkups:
        if checkup.date_start == datetime.today().date():
            checkup_list.append((checkup, True))
        else:
            checkup_list.append((checkup, False))

    context = {
        'checkups' : checkup_list
    }

    return render(request, 'unitmanagement/k9_checkup_list_today.html', context)

def k9_mia_list(request):

    k9_mia = K9.objects.filter(training_status = "MIA")

    context = {
        'k9_mia' : k9_mia
    }

    return render(request, 'unitmanagement/k9_mia_list.html', context)