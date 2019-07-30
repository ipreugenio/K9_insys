from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_date

from .models import K9, K9_Past_Owner, K9_Donated, K9_Parent, K9_Quantity, Dog_Breed, K9_Supplier, K9_Litter, K9_Mated
from .forms import add_donated_K9_form, add_donator_form, add_K9_parents_form, add_offspring_K9_form, select_breeder, K9SupplierForm, date_mated_form, HistDateForm, DateForm,DateK9Form

from .forms import add_donated_K9_form, add_donator_form, add_K9_parents_form, add_offspring_K9_form, select_breeder, K9SupplierForm, date_mated_form, add_breed_form
from .models import K9, K9_Past_Owner, K9_Donated, K9_Parent, K9_Quantity, K9_Supplier, K9_Litter
from .models import K9_Mated
from .forms import DateForm
from deployment.models import Incidents, Daily_Refresher, Team_Dog_Deployed
from planningandacquiring.models import Proposal_Budget, Proposal_K9,Proposal_Milk_Food, Proposal_Vac_Prev, Proposal_Medicine, Proposal_Vet_Supply, Proposal_Kennel_Supply, Proposal_Others, Actual_Budget, Actual_K9,Actual_Milk_Food, Actual_Vac_Prev, Actual_Medicine, Actual_Vet_Supply, Actual_Kennel_Supply, Actual_Others

from django.db.models import Sum
from training.models import Training
from profiles.models import Account, User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.http import JsonResponse
from django.contrib import messages
from .forms import ReportDateForm, k9_detail_form, SupplierForm, ProcuredK9Form,k9_acquisition_form
from deployment.models import Dog_Request, Team_Assignment

from unitmanagement.models import Health, HealthMedicine, VaccinceRecord, VaccineUsed
from inventory.models import Food, Food_Subtracted_Trail, Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Miscellaneous, Miscellaneous_Subtracted_Trail, Food_Received_Trail, Medicine_Received_Trail, Miscellaneous_Received_Trail

from unitmanagement.models import Health, HealthMedicine, VaccinceRecord, VaccineUsed, Notification, Handler_Incident
from inventory.models import Food, Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Miscellaneous, Medicine_Received_Trail, Food_Received_Trail, Miscellaneous_Received_Trail

from django.db.models.functions import Trunc, TruncMonth, TruncYear, TruncDay
from django.db.models import aggregates, Avg, Count, Min, Sum, Q, Max
import dateutil.parser
#from faker import Faker

#statistical imports
from math import *
from decimal import Decimal
from sklearn.metrics import mean_squared_error


from datetime import datetime as dt

from datetime import timedelta

from datetime import date

# from faker import Faker
#
# #statistical imports
# from math import *
# from decimal import Decimal
# from sklearn.metrics import mean_squared_error
# import pandas as pd
# import numpy as np
#
# #graphing imports
# from igraph import *
# import plotly.offline as opy
# import plotly.graph_objs as go
# import plotly.graph_objs.layout as lout
#
# #forecasting imports
# from statsmodels.tsa.ar_model import AR
# from statsmodels.tsa.arima_model import ARMA
# from statsmodels.tsa.arima_model import ARIMA
# from statsmodels.tsa.statespace.sarimax import SARIMAX
# from statsmodels.tsa.holtwinters import SimpleExpSmoothing
# from statsmodels.tsa.holtwinters import ExponentialSmoothing
# from random import random, randint
# from statsmodels.tsa.stattools import adfuller, kpss
# import statsmodels.api as sm

import math
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

def user_session(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)
    return user_in_session

def index(request):
    next_year = dt.now().year + 1
    current_year = dt.now().year

    stat = True
    all_k9 = K9.objects.exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost")
    print(stat)

    #K9 to be born and die
    k9_breeded = K9_Mated.objects.filter(status='Pregnant')
    print(k9_breeded)
    ny_breeding = [] 
    ny_data = []
    for kb in k9_breeded:
        m = kb.date_mated  + timedelta(days=63)
        if m.year == next_year:
            ny = [kb.mother.breed, kb.mother.litter_no]
            ny_data.append(ny)
            ny_breeding.append(kb.mother.breed)
            #get k9, value, total count by breed
            
    kb_index = pd.Index(ny_breeding)

    b_values = kb_index.value_counts().keys().tolist() #k9 breed to be born
    b_counts = kb_index.value_counts().tolist() #number of k9 to be born by breed

    #Total count of all dogs born next year by breed,
    breed_u = np.unique(ny_breeding)

    p = pd.DataFrame(ny_data, columns=['Breed', 'Litter'])
    h = p.groupby(['Breed']).sum()

    total_born = []  
    total_born_count = []  
    for u in breed_u:
        total_born_count.append(h.loc[u].values[0])
        born = [u,h.loc[u].values[0]]
        total_born.append(born)

    ny_dead = []
    for kd in all_k9:
        b = Dog_Breed.objects.get(breed = kd.breed)
        if (kd.age + 1) >= b.life_span:
            ny_dead.append(kd.breed)
            

    kd_index = pd.Index(ny_dead)

    d_values = kd_index.value_counts().keys().tolist()
    d_counts = kd_index.value_counts().tolist()

    all_k = all_k9.values_list('breed', flat=True).order_by()

    all_ku = np.unique(all_k)

    all_dogs = K9.objects.exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()

    all_kk = []
    for a in all_ku:
        c = all_k9.filter(breed=a).count()
        cc = [a,c]
        all_kk.append(cc)

    k9_cy = all_dogs
    k9_ny = all_dogs - sum(d_counts)
    k9_t_ny = k9_cy+50

    difference_k9 = k9_cy - k9_ny
    born_ny=0
    for b in k9_breeded:
        d = Dog_Breed.objects.get(breed=b.mother.breed)
        born_ny = born_ny + d.litter_number

    # born_ny =  sum(total_born_count)

    need_procure_ny = (50 + difference_k9) - born_ny
    if need_procure_ny <= 0:
        need_procure_ny = 0

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {

        'notif_data':notif_data,
        'count':count,
        'user':user,

    }

    return render(request, 'planningandacquiring/index.html', context)

def budgeting_list(request):

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    data = Proposal_Budget.objects.all()
    if request.method == 'POST':
        pass

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data': data,
    }
    return render(request, 'planningandacquiring/budget_list.html', context)

def report(request):
    form = ReportDateForm()
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title' : "REPORT",
        'form': form,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        }
    return render (request, 'planningandacquiring/report.html', context)

def add_procured_k9(request):
    form = SupplierForm(request.POST or None)
    k9_formset = formset_factory(ProcuredK9Form, extra=1, can_delete=True)
    formset = k9_formset(request.POST, request.FILES)
    style = "ui green message"

    try:
        print(request.session['procured'])
    except:
        pass
    if request.method == "POST":
        if form.is_valid():
            supplier_data = form.cleaned_data['supplier']
            supplier = K9_Supplier.objects.get(name=supplier_data)

            if formset.is_valid():
                print("Formset is valid")
                for forms in formset:
                    cd = forms.cleaned_data
                    name = cd.get('name')
                    bday = cd.get('birth_date')
                    sex = cd.get('sex')
                    color = cd.get('color')
                    dhpp = cd.get('date_dhhp')
                    rabies = cd.get('date_rabies')
                    bordertella = cd.get('date_bordertela')
                    deworm = cd.get('date_deworm')

                    k9 = K9.objects.create(name=name,birth_date=bday,source='Procurement',training_status='Unclassified',sex=sex,color=color)
                    
                    VaccineUsed.objects.create(k9=k9,disease='DHPPiL4',date_vaccinated=dhpp,done=True)
                    
                    VaccineUsed.objects.create(k9=k9,disease='Anti-Rabies',date_vaccinated=rabies,done=True)
                    
                    VaccineUsed.objects.create(k9=k9,disease='Deworming',date_vaccinated=deworm,done=True)
                    
                    VaccineUsed.objects.create(k9=k9,disease='Bordetella',date_vaccinated=bordertella,done=True)
             
                style = "ui green message"
                messages.success(request, 'Procured K9s has been added!')
                
                return redirect('planningandacquiring:K9_list')
            else:
                print(formset.errors)
                style = "ui red message"
                messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title' : "Procured K9",
        'form': SupplierForm(),
        # 'formset':k9_formset(),
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'style':style,
        }
    return render (request, 'planningandacquiring/add_procured_k9.html', context)

def add_supplier(request):
    form = K9SupplierForm(request.POST)
    style = ''
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            form.save()

            style = "ui green message"
            messages.success(request, 'Supplier has been added!')
            form = K9SupplierForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

        form.initial['organization'] = None
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'title' : "Add K9 Supplier",
        'texthelp' : "Please input the Supplier information below.",
        'form': form,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'style':style,
        }
    return render (request, 'planningandacquiring/add_k9_supplier.html', context)

#Form format
def add_donated_K9(request):
    form = add_donated_K9_form(request.POST or None, request.FILES or None)
    style = "ui teal message"
    if request.method == 'POST':
        if form.is_valid():
            k9 = form.save()
            k9.training_status = "Unclassified"
            k9.source = "Procurement"
            k9.save()

            request.session['k9_id'] = k9.id


            return HttpResponseRedirect('confirm_donation/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
            print(form)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title' : "Add New K9",
        'form' : form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'planningandacquiring/add_donated_K9.html', context)

'''
def add_donator(request):
    form = add_donator_form(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        if form.is_valid():
            donator= form.save()

            request.session['donator_id'] = donator.id

            return HttpResponseRedirect('confirm_donation/')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'Title': "Receive Donated K9",
        'form': form,
        'style': style,
    }

    return render(request, 'planningandacquiring/add_donator.html', context)
'''

def confirm_donation(request):

    k9_id = request.session['k9_id']
    k9= K9.objects.get(id = k9_id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Add New K9",
        'k9': k9,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render(request, 'planningandacquiring/confirm_K9_donation.html', context)

def donation_confirmed(request):
    k9_id = request.session['k9_id']

    k9 = K9.objects.get(id=k9_id)
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    if 'ok' in request.POST:
        VaccinceRecord.objects.create(k9=k9, deworming_1=True, deworming_2=True, deworming_3=True,
                                      deworming_4=True, dhppil_cv_1=True, dhppil_cv_2=True, dhppil_cv_3=True,
                                      heartworm_1=True, heartworm_2=True,
                                      heartworm_3=True, heartworm_4=True, heartworm_5=True, heartworm_6=True,
                                      heartworm_7=True, heartworm_8=True,
                                      anti_rabies=True, bordetella_1=True, bordetella_2=True, dhppil4_1=True,
                                      dhppil4_2=True, tick_flea_1=True,
                                      tick_flea_2=True, tick_flea_3=True, tick_flea_4=True, tick_flea_5=True,
                                      tick_flea_6=True, tick_flea_7=True)

        return render(request, 'planningandacquiring/donation_confirmed.html', context)
    else:
        #delete k9
        k9.delete()

        #NOTIF SHOW
        notif_data = notif(request)
        count = notif_data.filter(viewed=False).count()
        user = user_session(request)
        context = {
            'Title': "Add New K9",
            'form': add_donated_K9_form,
            'notif_data':notif_data,
            'count':count,
            'user':user,
        }
        return render(request, 'planningandacquiring/add_donated_K9.html', context)

def breeding_list(request, id=None):
    data1 = K9_Mated.objects.filter(status='Breeding').order_by('-id', '-date_mated')
    data2 = K9_Mated.objects.filter(status='Pregnant').order_by('-id', '-date_mated')
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    data_id=id
    d = None
    if data_id!=None:
        d = K9_Mated.objects.get(id=id)
        data1 = K9_Mated.objects.filter(status='Breeding').exclude(id=id).order_by('-id', '-date_mated')
      
    context = {
        'Title': "Breeding List",
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data1':data1,
        'data2':data2,
        'data_id':data_id,
        'd':d,
        
    }
    return render(request, 'planningandacquiring/breeding_list.html', context)

def confirm_failed_pregnancy(request, id):
    data = K9_Mated.objects.get(id=id) # get k9
    mom = K9.objects.get(id=data.mother.id)
    decision = request.GET.get('decision')
    
    if decision == 'confirm':
        data.status = 'Pregnant'
        mom.training_status = 'Breeding'

        messages.success(request, 'You have confirmed that ' + str(data.mother) + 'is pregnent.')

    elif decision == 'failed':
        data.status = 'Failed'
        mom.training_status = 'For-Breeding'
        K9_Litter.objects.create(mother=data.mother, father=data.father, litter_no=0)
        
        messages.success(request, 'You have confirmed that ' + str(data.mother) + ' is not pregnant.')

    data.save()
    mom.save()

    return redirect('planningandacquiring:breeding_list')

def add_K9_parents(request):
    style = "ui teal message"
    mother  = K9.objects.filter(sex="Female").filter(training_status = "For-Breeding").filter(age__gte = 1).filter(age__lte = 6).filter(Q(reproductive_stage = "Estrus") | Q(reproductive_stage = "Proestrus"))
    
    father = K9.objects.filter(sex="Male").filter(training_status = "For-Breeding").filter(age__gte = 1).filter(age__lte = 6)
    mother_all  = K9.objects.filter(sex="Female").filter(training_status = "For-Breeding").filter(age__gte = 1).filter(age__lte = 6).exclude(Q(reproductive_stage = "Estrus") | Q(reproductive_stage = "Proestrus"))
    
    mom = []
    sick = []
    b_arr = []
    for m in mother:
        h = Health.objects.filter(dog=m).count()
        mom.append(m)
        sick.append(h)

        birth = K9_Litter.objects.filter(mother=m).aggregate(sum=Sum('litter_no'))['sum']
        death = K9_Litter.objects.filter(mother=m).aggregate(sum=Sum('litter_died'))['sum']

        if birth != None or death != None:
            total = (birth / (birth+death)) * 100
        else:
            total=100
        
        b_arr.append(int(total))

    mlist = zip(mom,sick,b_arr)


    mmom = []
    msick = []
    mb_arr = []
    for mm in mother_all:
        h = Health.objects.filter(dog=mm).count()
        mmom.append(mm)
        msick.append(h)

        birth = K9_Litter.objects.filter(mother=mm).aggregate(sum=Sum('litter_no'))['sum']
        death = K9_Litter.objects.filter(mother=mm).aggregate(sum=Sum('litter_died'))['sum']

        if birth != None or death != None:
            total = (birth / (birth+death)) * 100
        else:
            total=100
        
        mb_arr.append(int(total))

    mmlist = zip(mmom,msick,mb_arr)

    dad = []
    dsick = []
    db_arr = []
    for mm in father:
        h = Health.objects.filter(dog=mm).count()
        dad.append(mm)
        dsick.append(h)

        birth = K9_Litter.objects.filter(mother=mm).aggregate(sum=Sum('litter_no'))['sum']
        death = K9_Litter.objects.filter(mother=mm).aggregate(sum=Sum('litter_died'))['sum']

        if birth != None or death != None:
            total = (birth / (birth+death)) * 100
        else:
            total=100
        
        db_arr.append(int(total))

    flist = zip(dad,dsick,db_arr)

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

    if request.method == 'POST':
        f = request.POST.get('radiof')
        m = request.POST.get('radiom')

        request.session["mother_id"] = m
        request.session["father_id"] = f

        return redirect('planningandacquiring:confirm_K9_parents')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "K9_Breeding",
        'today': dt.today(),
        'style': style,
        'mlist' : mlist,
        'flist' : flist,
        'mmlist':mmlist,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        
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

    return render(request, 'planningandacquiring/add_K9_parents.html', context)

def in_heat_change(request):
    if request.method == 'POST':
        id = request.POST.get('id_k9')
        date = parse_date(request.POST.get('date_change'))
        
        k9 = K9.objects.get(id=id)
        k9.last_proestrus_date = date
        k9.save()
        
        return redirect('planningandacquiring:add_K9_parents_form')


def confirm_K9_parents(request):
    form = date_mated_form(request.POST or None)

    form.initial['date_mated'] = dt.today()
    mother_id = request.session["mother_id"]
    father_id = request.session["father_id"]

    mother = K9.objects.get(id=mother_id)
    father = K9.objects.get(id=father_id)

    request.session['date_mated'] = None

    if request.method == 'POST':
        if form.is_valid():
            mated = form.save(commit=False)
            mated.mother = mother
            mated.father = father
            mated.save()

            mother.training_status = 'Breeding'
            mother.save()
            request.session['date_mated'] = mated.id

        return redirect('planningandacquiring:breeding_list', id=mated.id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'mother': mother,
        'father': father,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'form':form,
    }

    return render(request, 'planningandacquiring/confirm_K9_parents.html', context)

def mating_confirmed(request):
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render(request, 'planningandacquiring/mating_confirmed.html', context)

def K9_parents_confirmed(request):
    mothers = K9.objects.filter(sex="Female")
    fathers = K9.objects.filter(sex="Male")

    mother_list = []
    father_list = []

    for mother in mothers:
        mother_list.append(mother)

    for father in fathers:
        father_list.append(father)

    if 'ok' in request.POST:
        return HttpResponseRedirect('add_K9_offspring_form/')
    else:
        #NOTIF SHOW
        notif_data = notif(request)
        count = notif_data.filter(viewed=False).count()
        user = user_session(request)
        context = {
            'Title': "Receive Donated K9",
            'form': add_K9_parents_form,
            'mothers': mother_list,
            'fathers': father_list,
            'notif_data':notif_data,
            'count':count,
            'user':user,
        }
        return render(request, 'planningandacquiring/add_K9_parents.html', context)

#TODO
#formset
def add_K9_offspring(request, id):
    form = DateK9Form(request.POST or None)
    k9_formset = formset_factory(add_offspring_K9_form, extra=1, can_delete=True)
    formset = k9_formset(request.POST, request.FILES)
    style = ''

    data = K9_Mated.objects.get(id=id)
    data.status = 'Pregnancy Done'
    if data.mother.breed != data.father.breed:
        breed = 'Mixed'
    else:
        breed = data.mother.breed

    k9_count = 0

    
    if request.method == 'POST':
        data.mother.training_status = 'For-Breeding'
        data.save()
        if form.is_valid():
            date = form.cleaned_data['birth_date']

        if formset.is_valid():
            for form in formset:
                k9 = form.save(commit=False)
                k9.source = "Breeding"
                k9.breed = breed
                k9.birth_date = date
                k9.save()
                
                #K9 parents create
                K9_Parent.objects.create(mother=data.mother, father=data.father, offspring=k9)

                k9_count = k9_count+1

            died =  request.POST.get('litter_died')
            K9_Litter.objects.create(mother=data.mother, father=data.father, litter_no=k9_count, litter_died=died)
            
            #Mom
            mom = K9.objects.get(id=data.mother.id)
            mom.training_status='For-Breeding'
            mom.save()
            #Dad
            dad = K9.objects.get(id=data.father.id)
            dad.save()

            data.save()
            messages.success(request, 'You have added k9 offspring!')
            return redirect('planningandacquiring:breeding_list')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')


    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Receive Donated K9",
        'form': form,
        # 'formset': k9_formset(),
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'data':data,
    }

    return render(request, 'planningandacquiring/add_K9_offspring.html', context)

def breeding_k9_confirmed(request):
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    return render(request, 'planningandacquiring/breeding_confirmed.html', context)

def confirm_breeding(request):
    offspring_id = request.session['offspring_id']
    mother_id = request.session['mother_id']
    father_id = request.session['father_id']

    offspring = K9.objects.get(id=offspring_id)
    mother = K9.objects.get(id=mother_id)
    father = K9.objects.get(id=father_id)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Receive Donated K9",
        'offspring': offspring,
        'mother': mother,
        'father': father,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'planningandacquiring/confirm_breeding.html', context)

def breeding_confirmed(request):
    offspring_id = request.session['offspring_id']
    mother_id = request.session['mother_id']
    father_id = request.session['father_id']

    offspring = K9.objects.get(id=offspring_id)
    mother = K9.objects.get(id=mother_id)
    father = K9.objects.get(id=father_id)

    if 'ok' in request.POST:
        k9_parent = K9_Parent(offspring = offspring, mother = mother, father = father)
        k9_parent.save()

        cvr = VaccinceRecord.objects.create(k9=offspring)
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='bordetella_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='deworming_4')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='bordetella_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='anti_rabies')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil_cv_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil4_1')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_3')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='dhppil4_2')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_4')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_4')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_5')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_5')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_6')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_6')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_7')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='tick_flea_7')
        VaccineUsed.objects.create(vaccine_record=cvr, disease='heartworm_8')


        #NOTIF SHOW
        notif_data = notif(request)
        count = notif_data.filter(viewed=False).count()
        context={
            'notif_data':notif_data,
            'count':count,
        }

        return render(request, 'planningandacquiring/breeding_confirmed.html', context)
    else:
        #delete offspring
        offspring.delete()

        mothers = K9.objects.filter(sex="Female")
        fathers = K9.objects.filter(sex="Male")

        mother_list = []
        father_list = []

        for mother in mothers:
            mother_list.append(mother)

        for father in fathers:
            father_list.append(father)

        #NOTIF SHOW
        notif_data = notif(request)
        count = notif_data.filter(viewed=False).count()
        user = user_session(request)
        context = {
            'Title': "Receive Donated K9",
            'form': add_K9_parents_form,
            'mothers': mother_list,
            'fathers': father_list,
            'notif_data':notif_data,
            'count':count,
            'user':user,
        }
        return render(request, 'planningandacquiring/add_K9_parents.html', context)


#Listview format
def K9_listview(request):

    k9 = K9.objects.all()
    style = 'ui green message'
    
    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title' : 'K9 List',
        'k9' : k9,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'style':style,
    }

    return render(request, 'planningandacquiring/K9_list.html', context)

#Detailview format
def K9_detailview(request, id):
    k9 = K9.objects.get(id = id)
    form = k9_detail_form(request.POST or None, request.FILES or None, instance=k9)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'K9 Details Updated!')

            if k9.training_status == 'For-Deployment' or k9.training_status == 'For-Breeding':
                k9.training_status = request.POST.get('radio')
                k9.save()

            return redirect('planningandacquiring:K9_detail', id = k9.id)

        # if 'change_training_status' in request.POST:
        #     print(request.POST.get('radio'))
        #     k9.training_status = request.POST.get('radio')
        #     k9.save()
        #     messages.success(request, 'K9 is now ' + k9.training_status + '!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    try:
        parent = K9_Parent.objects.get(offspring=k9)
    except K9_Parent.DoesNotExist:
        context = {
            'Title': 'K9 Details',
            'k9' : k9,
            'notif_data':notif_data,
            'count':count,
            'user':user,
            'form':form,
        }
    else:
        parent_exist = 1
        context = {
            'Title': 'K9 Details',
            'k9': k9,
            'parent': parent,
            'parent_exist': parent_exist,
            'notif_data':notif_data,
            'count':count,
            'user':user,
            'form':form,
        }

    return render(request, 'planningandacquiring/K9_detail.html', context)




def add_breed(request):
    form = add_breed_form(request.POST)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            breed = form.save()
            breed.save()
            style = "ui green message"
            messages.success(request, 'Breed has been successfully Added!')

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': "Add Breed",
        'form': form,
        'style': style,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }
    print(form)
    return render(request, 'planningandacquiring/add_breed.html', context)


def breed_listview(request):
    breed = Dog_Breed.objects.all()

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': 'Breed List',
        'breed': breed,
        'notif_data':notif_data,
        'count':count,
        'user':user,
    }

    return render(request, 'planningandacquiring/view_breed.html', context)


################# BUDGETING ###################

def choose_date(request):
    form = HistDateForm(request.POST or None)
    success = 0
    # if request.method == 'POST':
    #     if form.is_valid():
    #         year = request.POST.get('hist_date')
    #         request.session["session_year"] = year


    #         try:
    #             budget_alloc = Budget_allocation.objects.filter(date_created__year=year).latest('id')
    #             success = 1
    #         except:
    #             messages.success(request, 'Budget Estimate for this year does not exist!')

    # if success == 1:
    #     return HttpResponseRedirect('detailed_budget/')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()

    context = {
        'notif_data':notif_data,
        'count': count,
        'title': "",
        'form': form,
    }

    return render(request, 'planningandacquiring/choose_date.html', context)

def budgeting_detail(request, id):
    pb = Proposal_Budget.objects.get(id=id)
    pk9 = Proposal_K9.objects.filter(proposal=pb)
    mf = Proposal_Milk_Food.objects.filter(proposal=pb)
    vp = Proposal_Vac_Prev.objects.filter(proposal=pb)
    pm = Proposal_Medicine.objects.filter(proposal=pb)
    pvs = Proposal_Vet_Supply.objects.filter(proposal=pb)
    pks = Proposal_Kennel_Supply.objects.filter(proposal=pb)
    po = Proposal_Others.objects.filter(proposal=pb)

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    train_k9 = pb.k9_current +  pb.k9_needed + pb.k9_breeded

    # k9_val = pb.grand_total/train_k9

    ab = None
    ak9 = None
    amf = None
    avp = None
    am = None
    avs = None
    aks = None
    ao = None
    total_new = 0

    try: 
        pass
        ab = Actual_Budget.objects.get(year_budgeted__year=pb.year_budgeted.year)
        
        amf = Actual_Milk_Food.objects.filter(proposal=ab)
        ak9 = Actual_K9.objects.filter(proposal=ab)
        avp = Actual_Vac_Prev.objects.filter(proposal=ab)
        am = Actual_Medicine.objects.filter(proposal=ab)
        avs = Actual_Vet_Supply.objects.filter(proposal=ab)
        aks = Actual_Kennel_Supply.objects.filter(proposal=ab)
        ao = Actual_Others.objects.filter(proposal=ab)
        total_new = ab.k9_current + ab.k9_needed + ab.k9_breeded

    except ObjectDoesNotExist:
        ab = None

    if request.method == 'POST':
        lump_sum = request.POST.get('lump_sum')
        lump_sum = Decimal(lump_sum)
        
        petty_cash = 0
        food_milk_total = 0
        k9_total = 0
        vac_prev_total = 0
        medicine_total = 0
        vet_supply_total = 0
        kennel_total = 0
        others_total = 0
        training_total = 0
        grand_total = 0
        k9_value = 0
        k9_needed = 0
        ab = None
        try: 
            ab = Actual_Budget.objects.get(year_budgeted__year=pb.year_budgeted.year)
            Actual_K9.objects.filter(proposal=ab).delete()
            Actual_Milk_Food.objects.filter(proposal=ab).delete()
            Actual_Vac_Prev.objects.filter(proposal=ab).delete()
            Actual_Medicine.objects.filter(proposal=ab).delete()
            Actual_Vet_Supply.objects.filter(proposal=ab).delete()
            Actual_Kennel_Supply.objects.filter(proposal=ab).delete()
            Actual_Others.objects.filter(proposal=ab).delete()

            #k9
            for mfd in pk9:
                t_amount = lump_sum*mfd.percent # new total amount by percentage
                q_item = int(t_amount / mfd.price) # Quantity by new total amount 
                t_item = t_amount - (q_item*mfd.price) #total amount per item
                new_t_amount = q_item * mfd.price
                k9_total = k9_total + new_t_amount #Total Amount
                k9_needed = k9_needed + q_item # total count
                k9_value = k9_value + (t_amount/mfd.quantity) #k9 Value
                Actual_K9.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)

            #food 
            for mfd in mf:
                t_amount = lump_sum*mfd.percent # new total amount by percentage
                q_item = int(t_amount / mfd.price) # Quantity by new total amount 
                t_item = t_amount - (q_item*mfd.price) #total amount per item
                new_t_amount = q_item * mfd.price
                food_milk_total = food_milk_total + new_t_amount #Total Amount
                k9_value = k9_value + (t_amount/mfd.k9_count) #k9 Value
                Actual_Milk_Food.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)
                
                
            #vaccine
            for mfd in vp:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                vac_prev_total = vac_prev_total + new_t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Vac_Prev.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)
            
            #medicine
            for mfd in pm:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                medicine_total = medicine_total + new_t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Medicine.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)
            
            #vet supply
            for mfd in pvs:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                vet_supply_total = vet_supply_total + t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Vet_Supply.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)

            #kennel supply
            for mfd in pks:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                kennel_total = kennel_total + t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Kennel_Supply.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)

            #others
            for mfd in po:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                others_total = others_total + t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Others.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)

            temp_total = food_milk_total + vac_prev_total +medicine_total +vet_supply_total+ kennel_total+others_total+k9_total+ (pb.k9_current_train*18000)
         
            #save Actual Budget
            ab.k9_needed = k9_needed
            ab.k9_total = k9_total
            ab.food_milk_total = food_milk_total
            ab.vac_prev_total = vac_prev_total
            ab.medicine_total = medicine_total
            ab.vet_supply_total = vet_supply_total
            ab.kennel_total = kennel_total 
            ab.others_total = others_total
            ab.training_total = (k9_needed*18000) + (pb.k9_current_train*18000)
            ab.train_count = pb.k9_current_train + k9_needed
            ab.petty_cash = lump_sum - (temp_total+(k9_needed*18000))
            ab.grand_total = lump_sum
            ab.save()

        except ObjectDoesNotExist:
           
            ab = Actual_Budget.objects.create(k9_current=pb.k9_current,k9_breeded=pb.k9_breeded,grand_total=lump_sum,year_budgeted=pb.year_budgeted)

            for mfd in pk9:
                t_amount = lump_sum*mfd.percent # new total amount by percentage
                q_item = int(t_amount / mfd.price) # Quantity by new total amount 
                t_item = t_amount - (q_item*mfd.price) #total amount per item
                new_t_amount = q_item * mfd.price
                k9_total = k9_total + new_t_amount #Total Amount
                k9_value = k9_value + (t_amount/mfd.quantity) #k9 Value
                Actual_K9.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)
                
            #food 
            for mfd in mf:
                t_amount = lump_sum*mfd.percent # new total amount by percentage
                q_item = int(t_amount / mfd.price) # Quantity by new total amount 
                t_item = t_amount - (q_item*mfd.price) 
                new_t_amount = q_item * mfd.price #total amount per item
                food_milk_total = food_milk_total + new_t_amount #Total Amount
                k9_value = k9_value + (t_amount/mfd.k9_count) #k9 Value
                Actual_Milk_Food.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)

            #vaccine
            for mfd in vp:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                vac_prev_total = vac_prev_total + new_t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Vac_Prev.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)
            
            #medicine
            for mfd in pm:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                medicine_total = medicine_total + new_t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Medicine.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)
            
            #vet supply
            for mfd in pvs:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                vet_supply_total = vet_supply_total + new_t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Vet_Supply.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)

            #kennel supply
            for mfd in pks:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                kennel_total = kennel_total + new_t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Kennel_Supply.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)

            #others
            for mfd in po:
                t_amount = lump_sum*mfd.percent
                q_item = int(t_amount / mfd.price)
                t_item = t_amount - (q_item*mfd.price)
                new_t_amount = q_item * mfd.price
                others_total = others_total + new_t_amount
                k9_value = k9_value + (t_amount/mfd.k9_count)
                Actual_Others.objects.create(item=mfd.item,quantity=q_item,price=mfd.price,total=new_t_amount,percent=mfd.percent,proposal=ab)

            temp_total = food_milk_total + vac_prev_total +medicine_total +vet_supply_total+ kennel_total+others_total+k9_total+ (pb.k9_current_train*18000)
         
            #save Actual Budget
            ab.k9_needed = k9_needed
            ab.k9_total = k9_total
            ab.food_milk_total = food_milk_total
            ab.vac_prev_total = vac_prev_total
            ab.medicine_total = medicine_total
            ab.vet_supply_total = vet_supply_total
            ab.kennel_total = kennel_total 
            ab.others_total = others_total
            ab.training_total = (k9_needed*18000) + (pb.k9_current_train*18000)
            ab.train_count = pb.k9_current_train + k9_needed
            ab.petty_cash = lump_sum - (temp_total+(k9_needed*18000))
            ab.grand_total = lump_sum
            ab.save()

        return redirect('planningandacquiring:budgeting_detail', id = id)
           
        # print('CURRENT:',pb.k9_current)
        # print('BREEDED:',pb.k9_breeded)
        # print('FOOD MILK: ', food_milk_total)
        # print('VACCINE: ', vac_prev_total)
        # print('MEDICINE: ', medicine_total)
        # print('VET SUPPLY: ', vet_supply_total)
        # print('KENNEL SUPPLY: ', kennel_total)
        # print('OTHERS: ', others_total)
        # print('TOTAL: ', lump_sum)
        # print('PETTY CASH: ', petty_cash)
        # print('TRAINING TOTAL: ', train_t)
        # print('NEEDED  K9: ', k9_needed)
        # print('TOTAL  K9: ', total_k9)

    context = {
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'pk9':pk9,
        'ak9':ak9,
        'pb':pb,
        'mf':mf,
        'vp':vp,
        'pm':pm,
        'pvs':pvs,
        'pks':pks,
        'po':po,
        'train_k9':train_k9,
        'ab':ab,
        'amf':amf,
        'avp':avp,
        'am':am,
        'avs':avs,
        'aks':aks,
        'ao':ao,
        'total_new':total_new,
    }
    return render(request, 'planningandacquiring/budgeting_detail.html', context)

def breed_list(request):
    breed = Dog_Breed.objects.all()

    # NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'Title': 'Breed List',
        'breed': breed,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/breed_list.html', context)

def breed_detail(request, id):
    breed = K9_Breed.objects.get(id=id)

    form = add_breed_form(request.POST or None, request.FILES or None, instance=breed)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Breed Details Updated!')

            return redirect('planningandacquiring:breed_detail', id=breed.id)

    # NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {
        'Title': 'Breed List',
        'breed': breed,
        'notif_data': notif_data,
        'count': count,
        'user': user,
        'form': form,
    }
    return render(request, 'planningandacquiring/breed_detail.html', context)


def budgeting_report(request):
 
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    context = {
        'notif': notif,
        'count': count,
    }

    return render(request, 'planningandacquiring/budgeting_report.html', context)
    
def detailed_budgeting(request):
 

    context = {
    
    }

    return render(request, 'planningandacquiring/detailed_budgeting.html', context)

################# END BUDGETING ###################

def accomplishment_date(request):
    form = DateForm(request.POST or None)

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        request.session["from_date"] = from_date
        request.session["to_date"] = to_date
        return HttpResponseRedirect('accomplishment_report/')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'form': form,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/accomplishment_date.html', context)

def accomplishment_report(request):
    from_date = request.session["from_date"]
    to_date = request.session["to_date"]

    explosives = Incidents.objects.filter(date__range=[from_date, to_date]).filter(type = "Explosives Related")
    narcotics = Incidents.objects.filter(date__range=[from_date, to_date]).filter(type = "Narcotics Related")
    sar = Incidents.objects.filter(date__range=[from_date, to_date]).filter(type = "Search and Rescue Related")
    others = Incidents.objects.filter(date__range=[from_date, to_date]).filter(type="Others")


    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {
        'from_date': from_date,
        'to_date': to_date,
        'explosives': explosives,
        'narcotics': narcotics,
        'sar': sar,
        'others': others,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/accomplishment_report.html', context)

def vet_date(request):
    form = DateForm(request.POST or None)

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        request.session["from_date"] = from_date
        request.session["to_date"] = to_date
        return HttpResponseRedirect('vet_report/')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'form': form,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/vet_date.html', context)

def vet_report(request):
    from_date = request.session["from_date"]
    to_date = request.session["to_date"]
    user = user_session(request)

    # VACCINES USED

    vaccineused = VaccineUsed.objects.filter(date_vaccinated__range=[from_date, to_date])

    vu_data=[]

    vu_disinct = vaccineused.values('vaccine').distinct()

    for vu in vu_disinct:
        for key,value in vu.items():
            print(value)
            v = vaccineused.filter(vaccine__id=value).count()
            vac = vaccineused.filter(vaccine__id=value).latest('date')
            arr = [vac.vaccine,vac.disease,v]
            vu_data.append(arr)

    print(vu_disinct)

    # MEDICINES USED

    health = Health.objects.filter(date_done__range=[from_date, to_date])
    med_used = HealthMedicine.objects.filter(health__in=health)

    med_data = []

    med_distinct = med_used.values('medicine').distinct()

    for med in med_distinct:
        for key, value in med.items():
            print(value)
            k9_count = med_used.filter(medicine__id=value).count()
            medi = med_used.filter(medicine__id=value).latest('id')
            print(medi)
            arr = [medi.medicine, k9_count]
            med_data.append(arr)

    print(k9_count)
    print(med_distinct)

    # SICKNESS

    health = Health.objects.filter(date__range=[from_date, to_date])
    health_distinct = health.values('problem').distinct()
    sick_data = []

    for sick in health_distinct:
        for key, value in sick.items():
            print(value)
            health_count = Health.objects.filter(problem=value).count()
            sickness = Health.objects.filter(problem=value).latest('id')

            arr = [sickness.problem, health_count]
            sick_data.append(arr)


            print(sick_data)
            print(health_distinct)
            print(health_count)

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)

    context = {
        'from_date': from_date,
        'to_date': to_date,
        'user': user,
        'vu_data': vu_data,
        'med_data': med_data,
        'sick_data': sick_data,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/vet_report.html', context)

def inventory_date(request):
    form = DateForm(request.POST or None)

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        request.session["from_date"] = from_date
        request.session["to_date"] = to_date
        return HttpResponseRedirect('inventory_report/')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'form': form,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/inventory_date.html', context)


def inventory_report(request):
    from_date = request.session["from_date"]
    to_date = request.session["to_date"]
    user = user_session(request)

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'from_date': from_date,
        'to_date': to_date,
        'user': user,

    }

    return render(request, 'planningandacquiring/inventory_report.html', context)

def deployment_date(request):
    form = DateForm(request.POST or None)

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        request.session["from_date"] = from_date
        request.session["to_date"] = to_date
        return HttpResponseRedirect('deployment_report/')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'form': form,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/deployment_date.html', context)


def deployment_report(request):
    from_date = request.session["from_date"]
    to_date = request.session["to_date"]
    user = user_session(request)

    locations = Incidents.objects.filter(date__range=[from_date, to_date])

    incidents_data = []

    incidents_distinct = locations.values('location').distinct()

    for loc in incidents_distinct:
        for key, value in loc.items():
            print(value)
            print(incidents_distinct)
            explosives = locations.filter(location__id=value).filter(type="Explosives Related").count()
            narcotics = locations.filter(location__id=value).filter(type="Narcotics Related").count()
            sar = locations.filter(location__id=value).filter(type="Search and Rescue Related").count()
            vac = locations.filter(location__id=value).latest('date')
            arr = [vac.location, explosives, narcotics, sar]
            incidents_data.append(arr)


    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'from_date': from_date,
        'to_date': to_date,
        'user': user,
        'incidents_data': incidents_data,

    }

    return render(request, 'planningandacquiring/deployment_report.html', context)

def handler_date(request):
    form = DateForm(request.POST or None)

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        request.session["from_date"] = from_date
        request.session["to_date"] = to_date
        return HttpResponseRedirect('handler_report/')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'form': form,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/handler_date.html', context)


def handler_report(request):
    from_date = request.session["from_date"]
    to_date = request.session["to_date"]
    user = user_session(request)

    handler = Handler_Incident.objects.filter(date__range=[from_date, to_date])

    handler_data = []

    handler_disinct = handler.values('handler').distinct()

    for h in handler_disinct:
        for key, value in h.items():
            print(value)
            positive = handler.filter(Q(incident = "Made an Arrest") | Q(incident="Rescued People")).count()
            negative = handler.filter(Q(incident="Poor Performance") | Q(incident="Violation") | Q(incident="Accident") | Q(
                incident="MIA") | Q(incident="Died")).count()
            handler_name = handler.filter(handler=value).latest('date')
            arr = [handler_name.handler, positive, negative]
            handler_data.append(arr)

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'from_date': from_date,
        'to_date': to_date,
        'user': user,
        'handler_data': handler_data,

    }

    return render(request, 'planningandacquiring/handler_report.html', context)

def k9_report(request):
    # from_date = request.session["from_date"]
    # to_date = request.session["to_date"]
    user = user_session(request)

    puppy = K9.objects.filter(training_status="Puppy").count()
    unclassified = K9.objects.filter(training_status="Unclassified").count()
    classified = K9.objects.filter(training_status="Classified").count()
    on_training = K9.objects.filter(training_status="On-Training").count()
    trained = K9.objects.filter(training_status="Trained").count()
    for_breeding = K9.objects.filter(training_status="For-Breeding").count()
    for_deployment = K9.objects.filter(training_status="For-Deployment").count()
    breeding = K9.objects.filter(training_status="Breeding").count()
    for_adoption = K9.objects.filter(training_status="For-Adoption").count()
    adopted = K9.objects.filter(training_status="adopted").count()
    deployed = K9.objects.filter(training_status="Deployed").count()
    light_duty = K9.objects.filter(training_status="Light Duty").count()
    retired = K9.objects.filter(training_status="Retired").count()
    dead = K9.objects.filter(training_status="Dead").count()


    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'user': user,
        'puppy': puppy,
        'unclassified': unclassified,
        'classified': classified,
        'on_training': on_training,
        'trained':trained,
        'for_breeding': for_breeding,
        'for_deployment': for_deployment,
        'breeding': breeding,
        'for_adoption': for_adoption,
        'adopted': adopted,
        'deployed': deployed,
        'light_duty': light_duty,
        'retired': retired,
        'dead': dead,
    }

    return render(request, 'planningandacquiring/k9_report.html', context)

def k9_performance_date(request):
    form = DateForm(request.POST or None)

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        request.session["from_date"] = from_date
        request.session["to_date"] = to_date
        return HttpResponseRedirect('k9_performance_report/')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'form': form,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/k9_performance_date.html', context)


def k9_performance_report(request):
    from_date = request.session["from_date"]
    to_date = request.session["to_date"]
    user = user_session(request)

    dog = Handler_Incident.objects.filter(date__range=[from_date, to_date])
    dog_data = []
    dog_disinct = dog.values('k9').distinct()

    for d in dog_disinct:
        for key, value in d.items():
            print(value)
            positive = dog.filter(Q(incident = "Made an Arrest") | Q(incident="Rescued People")).count()
            negative = dog.filter(Q(incident="Poor Performance") | Q(incident="Violation") | Q(incident="Accident") | Q(
                incident="MIA") | Q(incident="Died")).count()
            dog_name = dog.filter(k9=value).latest('date')
            arr = [dog_name.k9, positive, negative]
            dog_data.append(arr)

    refresher = Daily_Refresher.objects.filter(date__range=[from_date, to_date])
    dog_data = []
    dog_disinct = dog.values('k9').distinct()

    for d in dog_disinct:
        for key, value in d.items():
            print(value)
            positive = dog.filter(Q(incident="Made an Arrest") | Q(incident="Rescued People")).count()
            negative = dog.filter(Q(incident="Poor Performance") | Q(incident="Violation") | Q(incident="Accident") | Q(
                incident="MIA") | Q(incident="Died")).count()
            dog_name = dog.filter(k9=value).latest('date')
            arr = [dog_name.k9, positive, negative]
            dog_data.append(arr)

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'from_date': from_date,
        'to_date': to_date,
        'user': user,
        'dog_data': dog_data,

    }

    return render(request, 'planningandacquiring/k9_performance_report.html', context)

def dog_request_date(request):
    form = DateForm(request.POST or None)

    if request.method == 'POST':
        from_date = request.POST['from_date']
        to_date = request.POST['to_date']
        request.session["from_date"] = from_date
        request.session["to_date"] = to_date
        return HttpResponseRedirect('dog_request_report/')

    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'form': form,
        'notif_data': notif_data,
        'count': count,
        'user': user,
    }

    return render(request, 'planningandacquiring/dog_request_date.html', context)


def dog_request_report(request):
    from_date = request.session["from_date"]
    to_date = request.session["to_date"]
    user = user_session(request)

    event = Dog_Request.objects.filter(start_date__range=[from_date, to_date])
    event_data = []
    event_distinct = event.values('requester').distinct()

    deployed = Team_Dog_Deployed.objects.filter(date_added__range=[from_date, to_date])
    dog_distinct = deployed.values('k9').distinct()
    dog_data = []

    for d in dog_distinct:
        for key, value2 in d.items():
            print(value2)
            print(dog_distinct)
            SAR = K9.objects.filter(k9__id=value2).filter(capability="SAR").count()
            NDD = K9.objects.filter(k9__id=value2).filter(capability="NDD").count()
            EDD = K9.objects.filter(k9__id=value2).filter(capability="EDD").count()
            print(SAR)
            print(NDD)
            print(EDD)
            print("HELLO")

    for e in event_distinct:
        for key, value in e.items():
            print(value)
            print(event_distinct)

            event = event.filter(requester=value).latest('start_date')
            arr = [event.event_name, event.k9s_needed, event.k9s_deployed, SAR, NDD, EDD]
            event_data.append(arr)


    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'from_date': from_date,
        'to_date': to_date,
        'user': user,
        'event_data': event_data,

    }

    return render(request, 'planningandacquiring/dog_request_report.html', context)

def training_report(request):
    # from_date = request.session["from_date"]
    # to_date = request.session["to_date"]
    user = user_session(request)

    belgian_NDD = K9.objects.filter(trained="Trained").filter(breed="Belgian Malinois").filter(capability="NDD").count()
    belgian_EDD = K9.objects.filter(trained="Trained").filter(breed="Belgian Malinois").filter(capability="EDD").count()
    belgian_SAR = K9.objects.filter(trained="Trained").filter(breed="Belgian Malinois").filter(capability="SAR").count()
    total_belgian = K9.objects.filter(trained="Trained").filter(breed="Belgian Malinois").count()

    dutch_NDD = K9.objects.filter(trained="Trained").filter(breed="Dutch Sheperd").filter(capability="NDD").count()
    dutch_EDD = K9.objects.filter(trained="Trained").filter(breed="Dutch Sheperd").filter(capability="EDD").count()
    dutch_SAR = K9.objects.filter(trained="Trained").filter(breed="Dutch Sheperd").filter(capability="SAR").count()
    total_dutch = K9.objects.filter(trained="Trained").filter(breed="Dutch Sheperd").count()

    german_NDD = K9.objects.filter(trained="Trained").filter(breed="German Sheperd").filter(capability="NDD").count()
    german_EDD = K9.objects.filter(trained="Trained").filter(breed="German Sheperd").filter(capability="EDD").count()
    german_SAR = K9.objects.filter(trained="Trained").filter(breed="German Sheperd").filter(capability="SAR").count()
    total_german = K9.objects.filter(trained="Trained").filter(breed="German Sheperd").count()

    golden_NDD = K9.objects.filter(trained="Trained").filter(breed="Golden Retriever").filter(capability="NDD").count()
    golden_EDD = K9.objects.filter(trained="Trained").filter(breed="Golden Retriever").filter(capability="EDD").count()
    golden_SAR = K9.objects.filter(trained="Trained").filter(breed="Golden Retriever").filter(capability="SAR").count()
    total_golden = K9.objects.filter(trained="Trained").filter(breed="Golden Retriever").count()

    jack_NDD = K9.objects.filter(trained="Trained").filter(breed="Jack Russel").filter(capability="NDD").count()
    jack_EDD = K9.objects.filter(trained="Trained").filter(breed="Jack Russel").filter(capability="EDD").count()
    jack_SAR = K9.objects.filter(trained="Trained").filter(breed="Jack Russel").filter(capability="SAR").count()
    total_jack = K9.objects.filter(trained="Trained").filter(breed="Jack Russel").count()

    lab_NDD = K9.objects.filter(trained="Trained").filter(breed="Labrador Retriever").filter(capability="NDD").count()
    lab_EDD = K9.objects.filter(trained="Trained").filter(breed="Labrador Retriever").filter(capability="EDD").count()
    lab_SAR = K9.objects.filter(trained="Trained").filter(breed="Labrador Retriever").filter(capability="SAR").count()
    total_lab = K9.objects.filter(trained="Trained").filter(breed="Labrador Retriever").count()



    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'user': user,
        'belgian_NDD': belgian_NDD,
        'belgian_EDD': belgian_EDD,
        'belgian_SAR': belgian_SAR,

        'dutch_NDD': dutch_NDD,
        'dutch_EDD': dutch_EDD,
        'dutch_SAR': dutch_SAR,

        'german_NDD': german_NDD,
        'german_EDD': german_EDD,
        'german_SAR': german_SAR,

        'golden_NDD': golden_NDD,
        'golden_EDD': golden_EDD,
        'golden_SAR': golden_SAR,

        'jack_NDD': jack_NDD,
        'jack_EDD': jack_EDD,
        'jack_SAR': jack_SAR,

        'lab_NDD': lab_NDD,
        'lab_EDD': lab_EDD,
        'lab_SAR': lab_SAR,

        'total_belgian': total_belgian,
        'total_dutch': total_dutch,
        'total_german': total_german,
        'total_golden': total_golden,
        'total_jack': total_jack,
        'total_lab': total_lab,
    }

    return render(request, 'planningandacquiring/training_report.html', context)

###################################### AJAX LOAD FUNCTIONS ##################################################
def load_supplier(request):

    supplier = None

    try:
        supplier_id = request.GET.get('supplier')
        supplier = K9_Supplier.objects.get(id=supplier_id)
    except:
        pass
    context = {
        'supplier': supplier,
    }

    return render(request, 'planningandacquiring/supplier_data.html', context)

def load_k9_reco(request):

    h_count_arr = []
    k9_arr = []
    b_arr = []
    #TODO check
    try:
        id = request.GET.get('id')
        k9 = K9.objects.get(id=id)
       
        try:
            kp = K9_Parent.objects.filter(mother=k9)
            k9_o = K9_Parent.objects.get(offspring=k9)

            kp_id=[]
            for k in kp:
                kp_id.append(k.offspring.id)
            
            k9_m = K9_Parent.objects.filter(mother=k9_o.mother)
            k9_f = K9_Parent.objects.filter(father=k9_o.father)
            
            for m in k9_m:
                kp_id.append(m.offspring.id)

            for f in k9_f:
                kp_id.append(f.offspring.id)
        except ObjectDoesNotExist:
            kp_id = None

        print(kp_id)

        if kp_id != None:
            k9_data = K9.objects.filter(sex="Male").filter(training_status = "For-Breeding").filter(breed=k9.breed).filter(capability=k9.capability).filter(age__gte= 1).exclude(id__in=kp_id).order_by('-litter_no')
        else:
            k9_data = K9.objects.filter(sex="Male").filter(training_status = "For-Breeding").filter(breed=k9.breed).filter(capability=k9.capability).filter(age__gte= 1).order_by('-litter_no')
        
        print(k9_data)
        for k in k9_data:
            h_count = Health.objects.filter(dog=k).count()
            h_count_arr.append(h_count)   
            k9_arr.append(k)

            birth = K9_Litter.objects.filter(father=k).aggregate(sum=Sum('litter_no'))['sum']
            death = K9_Litter.objects.filter(father=k).aggregate(sum=Sum('litter_died'))['sum']

            if birth != None or death != None:
                total = (birth / (birth+death)) * 100
            else:
                total=100
            
            b_arr.append(int(total))

    except:
        pass

    flist = zip(k9_arr,h_count_arr, b_arr)

    context = {
        'k9': k9,
        'flist':flist,
    }

    return render(request, 'planningandacquiring/breeding_reco_data.html', context)
    
def load_health(request):

    health = None
    k9 = None
    try:
        k9 = request.GET.get('k9')
        k9_id = request.GET.get('id')
        health = Health.objects.filter(dog__id=k9_id) 
    except:
        pass

    context = {
        'health': health,
        'k9': k9,
    }

    return render(request, 'planningandacquiring/health_data.html', context)

def load_form(request):
    formset = None
    try:
        num = request.GET.get('num')
        print(num)
        k9_formset = formset_factory(add_offspring_K9_form, extra=int(num), can_delete=False)
        formset = k9_formset(request.POST, request.FILES)
    except:
        pass

    context = {
        'formset': k9_formset(),
    }

    return render(request, 'planningandacquiring/offspring_form_data.html', context)

def load_form_procured(request):
    formset = None
    formset2 = None
    try:
        num = request.GET.get('num')
        num = int(num)
        k9_formset = formset_factory(ProcuredK9Form, extra=num, can_delete=False)
        formset = k9_formset(request.POST, request.FILES)

    except:
        pass

    context = {
        'formset': k9_formset(),
    }

    return render(request, 'planningandacquiring/procured_form_data.html', context)

def load_budget_data(request):
    breed = None
    try:
        breed_id = request.GET.get('id')
        db = Dog_Breed.objects.get(id=breed_id)
      
    except:
        pass

    data = {
        'breed':db.id,
        'value':db.value,
    }

    return JsonResponse(data)

def budgeting(request):
    k9_formset = formset_factory(k9_acquisition_form, extra=1, can_delete=True)
    formset = k9_formset(request.POST, request.FILES)
    next_year = dt.now().year + 1
    current_year = dt.now().year

    need_procure_ny = 0

    stat = True
    all_k9 = K9.objects.exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost")
    print(stat)

    #K9 to be born and die
    k9_breeded = K9_Mated.objects.filter(status='Pregnant')
    print(k9_breeded)
    ny_breeding = [] 
    ny_data = []
    for kb in k9_breeded:
        m = kb.date_mated  + timedelta(days=63)
        if m.year == next_year:
            ny = [kb.mother.breed, kb.mother.litter_no]
            ny_data.append(ny)
            ny_breeding.append(kb.mother.breed)
            #get k9, value, total count by breed
            
    kb_index = pd.Index(ny_breeding)

    b_values = kb_index.value_counts().keys().tolist() #k9 breed to be born
    b_counts = kb_index.value_counts().tolist() #number of k9 to be born by breed

    #Total count of all dogs born next year by breed,
    breed_u = np.unique(ny_breeding)

    p = pd.DataFrame(ny_data, columns=['Breed', 'Litter'])
    h = p.groupby(['Breed']).sum()

    total_born = []  
    total_born_count = []  
    for u in breed_u:
        total_born_count.append(h.loc[u].values[0])
        born = [u,h.loc[u].values[0]]
        total_born.append(born)

    ny_dead = []
    for kd in all_k9:
        b = Dog_Breed.objects.get(breed = kd.breed)
        if (kd.age + 1) >= b.life_span:
            ny_dead.append(kd.breed)
            

    kd_index = pd.Index(ny_dead)
    #TODO
    # dead values and count
    d_values = kd_index.value_counts().keys().tolist()
    d_counts = kd_index.value_counts().tolist()

    # print(d_values)
    # print(d_counts)
    dead_list = zip(d_values,d_counts)


    all_k = all_k9.values_list('breed', flat=True).order_by()

    all_ku = np.unique(all_k)

    all_dogs = K9.objects.exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()

    all_kk = []
    for a in all_ku:
        c = all_k9.filter(breed=a).count()
        cc = [a,c]
        all_kk.append(cc)

    k9_cy = all_dogs
    k9_ny = all_dogs - sum(d_counts)
    k9_t_ny = k9_cy+50

    difference_k9 = k9_cy - k9_ny
    born_ny=0
    for b in k9_breeded:
        d = Dog_Breed.objects.get(breed=b.mother.breed)
        born_ny = born_ny + d.litter_number

     
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

    sar = Dog_Breed.objects.filter(skill_recommendation='SAR')
    ndd = Dog_Breed.objects.filter(skill_recommendation='NDD')
    edd = Dog_Breed.objects.filter(skill_recommendation='EDD')

    if request.method == "POST":
           
        need_procure_ny =  int(request.POST.get('id_need'))
        total_p =  Decimal(request.POST.get('id_need_total'))
        
        #get dog food based on dog count
        # k9 = all_k9 - dead + born + Forecasted added_procured
        # monthly 

        # 1L = 1000grams
        total_milk = born_ny *  21 #liter
        total_puppy_food = ((born_ny * 15) * 9) / 20 #sack
        total_adult_food = (need_procure_ny+k9_ny) * 12 #sack

        dog_food = []

        #end
        milk = Food_Subtracted_Trail.objects.filter(inventory__foodtype='Milk').latest('date_subtracted')
        puppy = Food_Subtracted_Trail.objects.filter(inventory__foodtype='Puppy Dog Food').filter(inventory__unit='Sack - 20kg').latest('date_subtracted')
        adult = Food_Subtracted_Trail.objects.filter(inventory__foodtype='Adult Dog Food').filter(inventory__unit='Sack - 20kg').latest('date_subtracted')
        
        #get current quantity
        sum_milk = Food.objects.filter(foodtype='Milk').aggregate(sum=Sum('quantity'))['sum']
        sum_puppy = Food.objects.filter(foodtype='Puppy Dog Food').aggregate(sum=Sum('quantity'))['sum']
        sum_adult = Food.objects.filter(foodtype='Adult Dog Food').aggregate(sum=Sum('quantity'))['sum']

        #milk
        tm = total_milk - sum_milk
        tmp = milk.inventory.price
        tmt = round((tm*tmp),2)

        #puppy
        tp = Decimal(total_puppy_food)- Decimal(sum_puppy)
        tpp = puppy.inventory.price
        tpt = round((tp*tpp),2)

        #adult
        ta = total_adult_food - sum_adult
        tap = adult.inventory.price
        tat = round((ta*tap),2)

        dm = [milk,tmp,int(tm),tmt,int(born_ny)]
        dp = [puppy,tpp,int(tp),tpt,int(born_ny)]
        da = [adult,tap,int(ta),tat,int(need_procure_ny+k9_ny)]
        
        if tmt > 0:
            dog_food.append(dm)
        if tpt > 0:
            dog_food.append(dp)
        if tat > 0:
            dog_food.append(da) 

        for (n,(item1,item2,item3,item4,item5)) in enumerate(dog_food):
            total_food =+ item4

        #MEDICINE EXPIRATION
        mrt = Medicine_Received_Trail.objects.filter(expiration_date__year=next_year).filter(status='Pending').values('inventory').annotate(sum = Sum('quantity'))

        med_item_id = []
        med_item_q = []
        for m in mrt: 
            for key,value in m.items():
                if key == 'inventory':
                    med_item_id.append(value)
                else:
                    med_item_q.append(value)

        zip_a = zip(med_item_id, med_item_q)

        # Medicine that has expirations next year
        ny_med = []
        cy_med = [] 
        eny_ar_count = 0
        eny_bbb_count = 0
        eny_dw_count = 0
        eny_dcv_count = 0
        eny_dc4_count = 0
        eny_hw_count = 0
        eny_tf_count = 0
        
        for a,b in zip_a:  
            c = Medicine_Inventory.objects.get(id=a)
            x = [c, (c.quantity - b)]
            z = [c, c.quantity]
            ny_med.append(x)
            cy_med.append(z)

            if c.medicine.immunization == 'Anti-Rabies':
                eny_ar_count = eny_ar_count + b
            elif c.medicine.immunization == 'Bordetella Bronchiseptica Bacterin':
                eny_bbb_count = eny_bbb_count + b
            elif c.medicine.immunization == 'Deworming':
                eny_dw_count = eny_dw_count + b
            elif c.medicine.immunization == 'DHPPiL+CV':
                eny_dcv_count = eny_dcv_count + b
            elif c.medicine.immunization == 'DHPPiL4':
                eny_dc4_count = eny_dc4_count + b
            elif c.medicine.immunization == 'Heartworm':
                eny_hw_count = eny_hw_count + b
            elif c.medicine.immunization == 'Tick and Flea':
                eny_tf_count = eny_tf_count + b

        #get all medicine used in the current year exclude vaccine
        mst_cy = Medicine_Subtracted_Trail.objects.filter(date_subtracted__year=current_year).exclude(inventory__medicine__med_type='Vaccine').exclude(inventory__medicine__med_type='Preventive').values('inventory').distinct()
        mst_ny = []
        np_arr = np.array(ny_med)
        for mst in mst_cy:
            for key,value in mst.items():
                if key == 'inventory':
                    c = Medicine_Inventory.objects.get(id=value)
                    if c in np_arr:
                        for (n, (item1, item2)) in enumerate(ny_med):
                            if c == item1:
                                a = [c, item2, c.medicine.price]
                                mst_ny.append(a)
                    else:
                        a = [c, c.quantity, c.medicine.price]
                        mst_ny.append(a)

        #med needed to procure next year and total
        b_ny_med = []
        total_medicine = 0
        for (n, (item1, item2, item3)) in enumerate(mst_ny):
            ms = Medicine_Subtracted_Trail.objects.filter(inventory=item1).aggregate(sum=Sum('quantity'))['sum']
            r = ms / k9_cy
            r = r * (k9_ny+born_ny+need_procure_ny) - item2

            if np.ceil(r) > 0:
                s = Decimal(np.ceil(r)) * Decimal(item3)
                ss = round(s, 2)
                b = [item1,item3,int(np.ceil(r)),ss,int((k9_ny+born_ny+need_procure_ny))]
                b_ny_med.append(b)
                total_medicine = total_medicine+ss
        
        # need_procure_ny == needed to be procured next year
        # born_ny == k9 born next year
        # k9_ny == k9 next year minus dead
        # k9_cy == k9 in current year

        #get all dogs that will be born/procured next year

        mst_vaccine_cy = Medicine_Subtracted_Trail.objects.filter(date_subtracted__year=current_year).filter(inventory__medicine__med_type='Vaccine').values('inventory').distinct().order_by('-date_subtracted')
        
        mst_vaccine_ny = []
        for mst in mst_vaccine_cy:
            for key,value in mst.items():
                if key == 'inventory':
                    c = Medicine_Inventory.objects.get(id=value)
                    # mst_arr = np.array(mst_vaccine_ny)
                    if not c.medicine.immunization in np.array(mst_vaccine_ny):
                        a = [c,c.medicine.immunization,c.medicine.price]
                        mst_vaccine_ny.append(a)

        if not 'Anti-Rabies' in np.array(mst_vaccine_ny):
            try:
                mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Anti-Rabies').values('inventory').annotate(sum=Sum('quantity'))

                inv = 0
                invq = 0
                temp =[]
                for i in mrt: 
                    for key,value in i.items():
                        if key == 'inventory':
                            i = value
                        if key == 'sum':
                            s = value
                            a = [i, s]
                            temp.append(a)

            #medicine inventory, count
                for (n, (item1,item2)) in enumerate(temp):
                    if item2 > invq:
                        inv = item1
                        inv1 = item2

                md = Medicine_Inventory.objects.get(id=inv)
                a = [md,md.medicine.immunization,md.medicine.price]
                mst_vaccine_ny.append(a)
            except:
                pass

        elif not 'Bordetella Bronchiseptica Bacterin' in np.array(mst_vaccine_ny):
            try:
                mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Bordetella Bronchiseptica Bacterin').values('inventory').annotate(sum=Sum('quantity'))

                inv = 0
                invq = 0
                temp =[]
                for i in mrt: 
                    for key,value in i.items():
                        if key == 'inventory':
                            i = value
                        if key == 'sum':
                            s = value
                            a = [i, s]
                            temp.append(a)

                #medicine inventory, count
                for (n, (item1,item2)) in enumerate(temp):
                    if item2 > invq:
                        inv = item1
                        inv1 = item2

                md = Medicine_Inventory.objects.get(id=inv)
                a = [md,md.medicine.immunization,md.medicine.price]
                mst_vaccine_ny.append(a)
            except:
                pass

        elif not 'DHPPiL+CV' in np.array(mst_vaccine_ny):
            try:
                mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='DHPPiL+CV').values('inventory').annotate(sum=Sum('quantity'))
                inv = 0
                invq = 0
                temp =[]
                for i in mrt: 
                    for key,value in i.items():
                        if key == 'inventory':
                            i = value
                        if key == 'sum':
                            s = value
                            a = [i, s]
                            temp.append(a)

                #medicine inventory, count
                for (n, (item1,item2)) in enumerate(temp):
                    if item2 > invq:
                        inv = item1
                        inv1 = item2

                md = Medicine_Inventory.objects.get(id=inv)
                a = [md,md.medicine.immunization,md.medicine.price]
                mst_vaccine_ny.append(a)
            except:
                pass

        elif not 'DHPPiL4' in np.array(mst_vaccine_ny):
            try:
                mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='DHPPiL4').values('inventory').annotate(sum=Sum('quantity'))
                inv = 0
                invq = 0
                temp =[]
                for i in mrt: 
                    for key,value in i.items():
                        if key == 'inventory':
                            i = value
                        if key == 'sum':
                            s = value
                            a = [i, s]
                            temp.append(a)

                #medicine inventory, count
                for (n, (item1,item2)) in enumerate(temp):
                    if item2 > invq:
                        inv = item1
                        inv1 = item2

                md = Medicine_Inventory.objects.get(id=inv)
                a = [md,md.medicine.immunization,md.medicine.price]
                mst_vaccine_ny.append(a)
            except:
                pass

        #item, quantity, total
        vac_ny = []


        #3 dhppil_cv, 1 anti rabies, 2 bordertella, 2 dhppil4,
        #3 anti rabies, bordertella, dhppil4,
        
        for (n, (item1, item2, item3)) in enumerate(mst_vaccine_ny):
            if item2 == 'Anti-Rabies':
                mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
                m = Medicine_Inventory.objects.get(id=item1.id)
                c = mi - eny_ar_count
                bn = int((born_ny + k9_ny) - c)
                pr = round(bn*m.medicine.price, 2)
                mi_a = [m,m.medicine.price,bn,pr,int(born_ny + k9_ny)]
                if pr > 0:
                    vac_ny.append(mi_a)
            elif item2 == 'Bordetella Bronchiseptica Bacterin':
                mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
                m = Medicine_Inventory.objects.get(id=item1.id)
                c = mi - eny_bbb_count
                bn = int(((born_ny*2) + k9_ny) - c)
                pr = round(bn*m.medicine.price, 2)
                mi_a = [m,m.medicine.price,bn,pr,int(born_ny + k9_ny)]
                if pr > 0:
                    vac_ny.append(mi_a)
            elif item2 == 'DHPPiL+CV':
                mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
                m = Medicine_Inventory.objects.get(id=item1.id)
                c = mi - eny_dcv_count
                bn = int(((born_ny*3) + k9_ny) - c)
                pr = round(bn*m.medicine.price, 2)
                mi_a = [m,m.medicine.price,bn,pr,int(born_ny + k9_ny)]
                if pr > 0:
                    vac_ny.append(mi_a)
            elif item2 == 'DHPPiL4':
                mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
                m = Medicine_Inventory.objects.get(id=item1.id)
                c = mi - eny_dc4_count
                bn = int(((born_ny*2) + k9_ny) - c)
                pr = round(bn*m.medicine.price, 2)
                mi_a = [m,m.medicine.price,bn,pr,int(born_ny + k9_ny)]
                if pr > 0:
                    vac_ny.append(mi_a)
        #4 deworming, 8 heartworm, 7 tick&flee

    # Deworming 
        try:
            data = Medicine_Subtracted_Trail.objects.filter(inventory__medicine__immunization='Deworming').values('inventory').annotate(sum=Sum('quantity'))
            print(data)
            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)
        
            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    invq = item2
            print(inv)
            md = Medicine_Inventory.objects.get(id=inv)
            dcq = Medicine_Inventory.objects.filter(medicine__immunization='Deworming').aggregate(sum=Sum('quantity'))['sum']
            dcq = dcq - eny_dw_count
            p_deworm = md.medicine.price
            q_deworm = int((born_ny * 7) + ((k9_ny+need_procure_ny) * 2) - dcq)
            t_deworm = p_deworm*q_deworm
            mi_a = [md,md.medicine.price,q_deworm,t_deworm,int(born_ny+k9_ny+need_procure_ny)]
            if t_deworm > 0:
                vac_ny.append(mi_a)

        except:
            data = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Deworming').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            dcq = Medicine_Inventory.objects.filter(medicine__immunization='Deworming').aggregate(sum=Sum('quantity'))['sum']
            dcq = dcq - eny_dw_count
            p_deworm = md.medicine.price
            q_deworm = int((born_ny * 7) + ((k9_ny+need_procure_ny) * 2) - dcq)
            t_deworm = p_deworm*q_deworm
            mi_a = [md,md.medicine.price,q_deworm,t_deworm,int(born_ny+k9_ny+need_procure_ny)]
            if t_deworm > 0:
                vac_ny.append(mi_a)

        # Heartworm
        try:
            data = Medicine_Subtracted_Trail.objects.filter(inventory__medicine__immunization='Heartworm').values('inventory').annotate(sum=Sum('quantity'))
            
            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            hcq = Medicine_Inventory.objects.filter(medicine__immunization='Heartworm').aggregate(sum=Sum('quantity'))['sum']
            hcq = hcq - eny_hw_count
            p_heatworm = md.medicine.price
            q_heatworm = int((born_ny * 8) + ((k9_ny+need_procure_ny) * 12) - hcq)
            t_heatworm = p_heatworm*q_heatworm
            mi_a = [md,md.medicine.price,q_heatworm,t_heatworm,int(born_ny+k9_ny+need_procure_ny)]
            if t_heatworm > 0:
                vac_ny.append(mi_a)
        except:
            data = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Heartworm').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            hcq = Medicine_Inventory.objects.filter(medicine__immunization='Heartworm').aggregate(sum=Sum('quantity'))['sum']
            hcq = hcq - eny_hw_count
            p_heatworm = md.medicine.price
            q_heatworm = int((born_ny * 8) + ((k9_ny+need_procure_ny) * 12) - hcq)
            t_heatworm = p_heatworm*q_heatworm
            mi_a = [md,md.medicine.price,q_heatworm,t_heatworm,int(born_ny+k9_ny+need_procure_ny)]
            if t_heatworm > 0:
                vac_ny.append(mi_a)

        # Tick & Flee
        try:
            data = Medicine_Subtracted_Trail.objects.filter(inventory__medicine__immunization='Tick and Flea').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            tcq = Medicine_Inventory.objects.filter(medicine__immunization='Tick and Flea').aggregate(sum=Sum('quantity'))['sum']
            tcq = tcq - eny_tf_count
            p_tickflea = md.medicine.price
            k_tf = k9_cy % 7
            q_tickflea = int((born_ny * 7 ) + ((k_tf/k9_cy) * (k9_ny+need_procure_ny)) - tcq)
            t_tickflea = round(Decimal(p_tickflea)*Decimal(q_tickflea), 2)
            mi_a = [md,md.medicine.price,q_tickflea,t_tickflea,int(born_ny+k9_ny+need_procure_ny)]
            if t_tickflea > 0:
                vac_ny.append(mi_a)
        except:
            data = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Tick and Flea').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            tcq = Medicine_Inventory.objects.filter(medicine__immunization='Tick and Flea').aggregate(sum=Sum('quantity'))['sum']
            tcq = tcq - eny_tf_count
            p_tickflea = md.medicine.price
            k_tf = k9_cy % 7
            q_tickflea = int((born_ny * 7 ) + ((k_tf/k9_cy) * (k9_ny+need_procure_ny)) - tcq)
            t_tickflea = round(Decimal(p_tickflea)*Decimal(q_tickflea), 2)
            mi_a = [md,md.medicine.price,q_tickflea,t_tickflea,int(born_ny+k9_ny+need_procure_ny)]
            if t_tickflea > 0:
                vac_ny.append(mi_a)

        vac_total = 0
        for (n, (item1, item2, item3,item4,item5)) in enumerate(vac_ny):
            vac_total = vac_total + item4
        #Vet Supply
        #item,quantity,total
        vet_arr=[]
        vet_total = 0
        mvi = Miscellaneous_Subtracted_Trail.objects.filter(inventory__misc_type="Vet Supply").filter(date_subtracted__year=current_year).values('inventory').distinct()

        for m in mvi: 
            for key,value in m.items():
                if key == 'inventory':
                    c = Miscellaneous.objects.get(id=value)
                    mvi_i = Miscellaneous_Subtracted_Trail.objects.filter(inventory=c).filter(date_subtracted__year=current_year).aggregate(sum=Sum('quantity'))['sum']
                    tq = int((mvi_i/k9_cy) * (k9_ny+need_procure_ny+born_ny))
                    tp = round(Decimal(tq)*Decimal(c.price), 2)
                    mv = [c,c.price, int(np.ceil(tq)), tp,int(born_ny+k9_ny+need_procure_ny)]
                    vet_total = vet_total+tp
                    vet_arr.append(mv)
        

        #Kennel supplies 
        #item,quantity,total
        ken_arr=[]
        ken_total = 0

        mki = Miscellaneous_Subtracted_Trail.objects.filter(inventory__misc_type="Kennel Supply").filter(date_subtracted__year=current_year).values('inventory').distinct()

        for m in mki: 
            for key,value in m.items():
                if key == 'inventory':
                    c = Miscellaneous.objects.get(id=value)
                    mvi_i = Miscellaneous_Subtracted_Trail.objects.filter(inventory=c).filter(date_subtracted__year=current_year).aggregate(sum=Sum('quantity'))['sum']
                    tq = int((mvi_i/k9_cy) * (k9_ny+need_procure_ny+born_ny))
                    tp = round(Decimal(tq)*Decimal(c.price), 2)
                    mv = [c,c.price, int(np.ceil(tq)), tp,int(born_ny+k9_ny+need_procure_ny)]
                    ken_total = ken_total+tp
                    ken_arr.append(mv)

        #get Others
        oth_arr = []
        oth_total = 0
        moi = Miscellaneous_Subtracted_Trail.objects.filter(inventory__misc_type="Others").filter(date_subtracted__year=current_year).values('inventory').distinct()
        #get all unique inventory and distribute to dogs

        for m in moi: 
            for key,value in m.items():
                if key == 'inventory':
                    c = Miscellaneous.objects.get(id=value)
                    mvi_i = Miscellaneous_Subtracted_Trail.objects.filter(inventory=c).filter(date_subtracted__year=current_year).aggregate(sum=Sum('quantity'))['sum']
                    tq = int((mvi_i/k9_cy) * (k9_ny+need_procure_ny+born_ny))
                    tp = round(Decimal(tq)*Decimal(c.price), 2)
                    mv = [c,c.price, int(np.ceil(tq)), tp,int(born_ny+k9_ny+need_procure_ny)]
                    oth_total = oth_total+tp
                    oth_arr.append(mv)

        #k9 current dog that needs funds for training
        mat_dog = K9.objects.filter(status='Material Dog').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count() + born_ny + need_procure_ny
        k9_current_train = K9.objects.filter(status='Material Dog').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()
        train_count = int(mat_dog)
        train_total = Decimal(mat_dog * 18000)
        
        train_arr = ['K9 Training',18000,mat_dog,train_total]

        grand_total=total_food+vac_total+total_medicine+vet_total+ken_total+oth_total+train_total+total_p
    
        try:
            pb = Proposal_Budget.objects.get(date_created__year=dt.today().year)
            pb.k9_current = k9_ny
            pb.k9_needed = need_procure_ny
            pb.k9_breeded = born_ny
            pb.food_milk_total = total_food
            pb.vac_prev_total = vac_total
            pb.medicine_total = total_medicine
            pb.vet_supply_total = vet_total
            pb.kennel_total = ken_total
            pb.others_total = oth_total
            pb.training_total = train_total
            pb.train_count = train_count
            pb.grand_total = grand_total
            pb.date_created = dt.today()
            pb.k9_current_train = k9_current_train
            pb.k9_total = total_p
            pb.save()

            Proposal_Milk_Food.objects.filter(proposal=pb).delete()
            Proposal_Vac_Prev.objects.filter(proposal=pb).delete()
            Proposal_Medicine.objects.filter(proposal=pb).delete()
            Proposal_Vet_Supply.objects.filter(proposal=pb).delete()
            Proposal_Kennel_Supply.objects.filter(proposal=pb).delete()
            Proposal_Others.objects.filter(proposal=pb).delete()
            Proposal_K9.objects.filter(proposal=pb).delete()
            
            #item, price, quantity, total
            for (n,(item1,item2,item3,item4,item5)) in enumerate(dog_food):
                percentage = Decimal(item4/grand_total)
                Proposal_Milk_Food.objects.create(item=item1.inventory, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)

            for (n, (item1, item2, item3,item4,item5)) in enumerate(vac_ny):
                percentage = Decimal(item4/grand_total)
                Proposal_Vac_Prev.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)
                
            for (n, (item1, item2, item3,item4,item5)) in enumerate(b_ny_med):
                percentage = Decimal(item4/grand_total)
                Proposal_Medicine.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)
                
            for (n, (item1, item2, item3,item4,item5)) in enumerate(vet_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Vet_Supply.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)
            
            for (n, (item1, item2, item3,item4,item5)) in enumerate(ken_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Kennel_Supply.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)
                
            for (n, (item1, item2, item3,item4,item5)) in enumerate(oth_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Others.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)

                #k9 formset

            if formset.is_valid():
                print("Formset is valid")
                for form in formset:
                    if form.is_valid():
                        f=form.save(commit=False)
                        f.percent = Decimal(f.total/grand_total)
                        f.proposal=pb
                        f.save()
                    
            
            return redirect('planningandacquiring:budget_list')
        except:
            pb = Proposal_Budget.objects.create(k9_current=k9_ny, k9_needed=need_procure_ny, k9_breeded=born_ny, food_milk_total=total_food, vac_prev_total=vac_total, medicine_total=total_medicine, vet_supply_total=vet_total, kennel_total=ken_total, others_total=oth_total, training_total=train_total, grand_total=grand_total, date_created=dt.today(),k9_current_train = k9_current_train,k9_total=total_p)

            #item, price, quantity, total
            for (n,(item1,item2,item3,item4,item5)) in enumerate(dog_food):
                percentage = Decimal(item4/grand_total)
                Proposal_Milk_Food.objects.create(item=item1.inventory, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)

            for (n, (item1, item2, item3,item4,item5)) in enumerate(vac_ny):
                percentage = Decimal(item4/grand_total)
                Proposal_Vac_Prev.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)
                
            for (n, (item1, item2, item3,item4,item5)) in enumerate(b_ny_med):
                percentage = Decimal(item4/grand_total)
                Proposal_Medicine.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)
                
            for (n, (item1, item2, item3,item4,item5)) in enumerate(vet_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Vet_Supply.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)
            
            for (n, (item1, item2, item3,item4,item5)) in enumerate(ken_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Kennel_Supply.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)
                
            for (n, (item1, item2, item3,item4,item5)) in enumerate(oth_arr):
                percentage = Decimal(item4/grand_total)
                Proposal_Others.objects.create(item=item1, price=item2,quantity=item3, total=item4,percent=percentage,proposal=pb,k9_count=item5)
                
            if formset.is_valid():
                print("Formset is valid")
                for form in formset:
                    if form.is_valid():
                        f=form.save(commit=False)
                        f.percent = Decimal(f.total/grand_total)
                        f.proposal=pb
                        f.save()

            return redirect('planningandacquiring:budget_list')
       
    #last year budget
    last_year = next_year - 2
    print(last_year)
    try:
        abb = Actual_Budget.objects.get(year_budgeted__year=last_year)
    except ObjectDoesNotExist:
        abb = None

    print(abb)

    #NOTIF SHOW
    notif_data = notif(request)
    count = notif_data.filter(viewed=False).count()
    user = user_session(request)
    context = {
        'abb':abb,
        'formset':k9_formset(),
        'today':dt.today(),
        'next_year':next_year,
        'notif_data':notif_data,
        'count':count,
        'user':user,
        'k9_cy': k9_cy,
        'k9_ny': k9_ny,
        'born_ny': born_ny,
        'dead_list':dead_list,
        'total_k9': born_ny+k9_ny,
        'NDD_count':NDD_count,
        'EDD_count':EDD_count,
        'SAR_count':SAR_count,
        'NDD_demand':NDD_demand,
        'EDD_demand':EDD_demand,
        'SAR_demand':SAR_demand,
        'sar':sar,
        'ndd':ndd,
        'edd':edd,
    }
    return render (request, 'planningandacquiring/budgeting.html', context)

def load_budget(request):
    total_p = None
    dog_food = None
    total_food = None
    vac_ny = None
    vac_total = None
    b_ny_med = None
    total_medicine = None
    vet_arr = None
    vet_total = None
    ken_arr = None
    ken_total = None
    oth_arr = None
    oth_total = None
    train_arr = None
    train_total = None
    grand_total = None
    stat = None
    try:   
        # formset = formset_factory(k9_acquisition_form, extra=1, can_delete=True)
        total_p = Decimal(request.GET.get('id_val'))
        need_procure_ny =  int(request.GET.get('p_count'))
        k9_ny =  int(request.GET.get('k9_ny'))
        born_ny =  int(request.GET.get('born_ny'))

        next_year = dt.now().year + 1
        current_year = dt.now().year

        stat = True
        all_k9 = K9.objects.exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost")
        print(stat)

        #K9 to be born and die
        k9_breeded = K9_Mated.objects.filter(status='Pregnant')
        print(k9_breeded)
        ny_breeding = [] 
        ny_data = []
        for kb in k9_breeded:
            m = kb.date_mated  + timedelta(days=63)
            if m.year == next_year:
                ny = [kb.mother.breed, kb.mother.litter_no]
                ny_data.append(ny)
                ny_breeding.append(kb.mother.breed)
                #get k9, value, total count by breed
                
        kb_index = pd.Index(ny_breeding)

        b_values = kb_index.value_counts().keys().tolist() #k9 breed to be born
        b_counts = kb_index.value_counts().tolist() #number of k9 to be born by breed

        #Total count of all dogs born next year by breed,
        breed_u = np.unique(ny_breeding)

        p = pd.DataFrame(ny_data, columns=['Breed', 'Litter'])
        h = p.groupby(['Breed']).sum()

        total_born = []  
        total_born_count = []  
        for u in breed_u:
            total_born_count.append(h.loc[u].values[0])
            born = [u,h.loc[u].values[0]]
            total_born.append(born)

        ny_dead = []
        for kd in all_k9:
            b = Dog_Breed.objects.get(breed = kd.breed)
            if (kd.age + 1) >= b.life_span:
                ny_dead.append(kd.breed)
                

        kd_index = pd.Index(ny_dead)

        d_values = kd_index.value_counts().keys().tolist()
        d_counts = kd_index.value_counts().tolist()

        all_k = all_k9.values_list('breed', flat=True).order_by()

        all_ku = np.unique(all_k)

        all_dogs = K9.objects.exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()

        all_kk = []
        for a in all_ku:
            c = all_k9.filter(breed=a).count()
            cc = [a,c]
            all_kk.append(cc)

        k9_cy = all_dogs
        k9_ny = all_dogs - sum(d_counts)
        k9_t_ny = k9_cy+50

        difference_k9 = k9_cy - k9_ny
        born_ny=0
        for b in k9_breeded:
            d = Dog_Breed.objects.get(breed=b.mother.breed)
            born_ny = born_ny + d.litter_number
        #get dog food based on dog count
        # k9 = all_k9 - dead + born + Forecasted added_procured
        # monthly 

        # 1L = 1000grams
        total_milk = born_ny *  21 #liter
        total_puppy_food = ((born_ny * 15) * 9) / 20 #sack
        total_adult_food = (need_procure_ny+k9_ny) * 12 #sack

        dog_food = []

        #end
        milk = Food_Subtracted_Trail.objects.filter(inventory__foodtype='Milk').latest('date_subtracted')
        puppy = Food_Subtracted_Trail.objects.filter(inventory__foodtype='Puppy Dog Food').filter(inventory__unit='Sack - 20kg').latest('date_subtracted')
        adult = Food_Subtracted_Trail.objects.filter(inventory__foodtype='Adult Dog Food').filter(inventory__unit='Sack - 20kg').latest('date_subtracted')
        
        #get current quantity
        sum_milk = Food.objects.filter(foodtype='Milk').aggregate(sum=Sum('quantity'))['sum']
        sum_puppy = Food.objects.filter(foodtype='Puppy Dog Food').aggregate(sum=Sum('quantity'))['sum']
        sum_adult = Food.objects.filter(foodtype='Adult Dog Food').aggregate(sum=Sum('quantity'))['sum']

        #milk
        tm = total_milk - sum_milk
        tmp = milk.inventory.price
        tmt = round((tm*tmp),2)

        #puppy
        tp = Decimal(total_puppy_food)- Decimal(sum_puppy)
        tpp = puppy.inventory.price
        tpt = round((tp*tpp),2)

        #adult
        ta = total_adult_food - sum_adult
        tap = adult.inventory.price
        tat = round((ta*tap),2)

        dm = [milk,tmp,int(tm),tmt,int(born_ny)]
        dp = [puppy,tpp,int(tp),tpt,int(born_ny)]
        da = [adult,tap,int(ta),tat,int(need_procure_ny+k9_ny)]
        
        if tmt > 0:
            dog_food.append(dm)
        if tpt > 0:
            dog_food.append(dp)
        if tat > 0:
            dog_food.append(da) 
    
        for (n,(item1,item2,item3,item4,item5)) in enumerate(dog_food):
            total_food =+ item4

        #MEDICINE EXPIRATION
        mrt = Medicine_Received_Trail.objects.filter(expiration_date__year=next_year).filter(status='Pending').values('inventory').annotate(sum = Sum('quantity'))

        med_item_id = []
        med_item_q = []
        for m in mrt: 
            for key,value in m.items():
                if key == 'inventory':
                    med_item_id.append(value)
                else:
                    med_item_q.append(value)

        zip_a = zip(med_item_id, med_item_q)

        # Medicine that has expirations next year
        ny_med = []
        cy_med = [] 
        eny_ar_count = 0
        eny_bbb_count = 0
        eny_dw_count = 0
        eny_dcv_count = 0
        eny_dc4_count = 0
        eny_hw_count = 0
        eny_tf_count = 0
        
        for a,b in zip_a:  
            c = Medicine_Inventory.objects.get(id=a)
            x = [c, (c.quantity - b)]
            z = [c, c.quantity]
            ny_med.append(x)
            cy_med.append(z)

            if c.medicine.immunization == 'Anti-Rabies':
                eny_ar_count = eny_ar_count + b
            elif c.medicine.immunization == 'Bordetella Bronchiseptica Bacterin':
                eny_bbb_count = eny_bbb_count + b
            elif c.medicine.immunization == 'Deworming':
                eny_dw_count = eny_dw_count + b
            elif c.medicine.immunization == 'DHPPiL+CV':
                eny_dcv_count = eny_dcv_count + b
            elif c.medicine.immunization == 'DHPPiL4':
                eny_dc4_count = eny_dc4_count + b
            elif c.medicine.immunization == 'Heartworm':
                eny_hw_count = eny_hw_count + b
            elif c.medicine.immunization == 'Tick and Flea':
                eny_tf_count = eny_tf_count + b

        #get all medicine used in the current year exclude vaccine
        mst_cy = Medicine_Subtracted_Trail.objects.filter(date_subtracted__year=current_year).exclude(inventory__medicine__med_type='Vaccine').exclude(inventory__medicine__med_type='Preventive').values('inventory').distinct()
        mst_ny = []
        np_arr = np.array(ny_med)
        for mst in mst_cy:
            for key,value in mst.items():
                if key == 'inventory':
                    c = Medicine_Inventory.objects.get(id=value)
                    if c in np_arr:
                        for (n, (item1, item2)) in enumerate(ny_med):
                            if c == item1:
                                a = [c, item2, c.medicine.price]
                                mst_ny.append(a)
                    else:
                        a = [c, c.quantity, c.medicine.price]
                        mst_ny.append(a)

        #med needed to procure next year and total
        b_ny_med = []
        total_medicine = 0
        for (n, (item1, item2, item3)) in enumerate(mst_ny):
            ms = Medicine_Subtracted_Trail.objects.filter(inventory=item1).aggregate(sum=Sum('quantity'))['sum']
            r = ms / k9_cy
            r = r * (k9_ny+born_ny+need_procure_ny) - item2

            if np.ceil(r) > 0:
                s = Decimal(np.ceil(r)) * Decimal(item3)
                ss = round(s, 2)
                b = [item1,item3,int(np.ceil(r)),ss,int((k9_ny+born_ny+need_procure_ny))]
                b_ny_med.append(b)
                total_medicine = total_medicine+ss
        
        # need_procure_ny == needed to be procured next year
        # born_ny == k9 born next year
        # k9_ny == k9 next year minus dead
        # k9_cy == k9 in current year

        #get all dogs that will be born/procured next year

        mst_vaccine_cy = Medicine_Subtracted_Trail.objects.filter(date_subtracted__year=current_year).filter(inventory__medicine__med_type='Vaccine').values('inventory').distinct().order_by('-date_subtracted')
        
        mst_vaccine_ny = []
        for mst in mst_vaccine_cy:
            for key,value in mst.items():
                if key == 'inventory':
                    c = Medicine_Inventory.objects.get(id=value)
                    # mst_arr = np.array(mst_vaccine_ny)
                    if not c.medicine.immunization in np.array(mst_vaccine_ny):
                        a = [c,c.medicine.immunization,c.medicine.price]
                        mst_vaccine_ny.append(a)

        if not 'Anti-Rabies' in np.array(mst_vaccine_ny):
            try:
                mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Anti-Rabies').values('inventory').annotate(sum=Sum('quantity'))

                inv = 0
                invq = 0
                temp =[]
                for i in mrt: 
                    for key,value in i.items():
                        if key == 'inventory':
                            i = value
                        if key == 'sum':
                            s = value
                            a = [i, s]
                            temp.append(a)

            #medicine inventory, count
                for (n, (item1,item2)) in enumerate(temp):
                    if item2 > invq:
                        inv = item1
                        inv1 = item2

                md = Medicine_Inventory.objects.get(id=inv)
                a = [md,md.medicine.immunization,md.medicine.price]
                mst_vaccine_ny.append(a)
            except:
                pass

        elif not 'Bordetella Bronchiseptica Bacterin' in np.array(mst_vaccine_ny):
            try:
                mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Bordetella Bronchiseptica Bacterin').values('inventory').annotate(sum=Sum('quantity'))

                inv = 0
                invq = 0
                temp =[]
                for i in mrt: 
                    for key,value in i.items():
                        if key == 'inventory':
                            i = value
                        if key == 'sum':
                            s = value
                            a = [i, s]
                            temp.append(a)

                #medicine inventory, count
                for (n, (item1,item2)) in enumerate(temp):
                    if item2 > invq:
                        inv = item1
                        inv1 = item2

                md = Medicine_Inventory.objects.get(id=inv)
                a = [md,md.medicine.immunization,md.medicine.price]
                mst_vaccine_ny.append(a)
            except:
                pass

        elif not 'DHPPiL+CV' in np.array(mst_vaccine_ny):
            try:
                mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='DHPPiL+CV').values('inventory').annotate(sum=Sum('quantity'))
                inv = 0
                invq = 0
                temp =[]
                for i in mrt: 
                    for key,value in i.items():
                        if key == 'inventory':
                            i = value
                        if key == 'sum':
                            s = value
                            a = [i, s]
                            temp.append(a)

                #medicine inventory, count
                for (n, (item1,item2)) in enumerate(temp):
                    if item2 > invq:
                        inv = item1
                        inv1 = item2

                md = Medicine_Inventory.objects.get(id=inv)
                a = [md,md.medicine.immunization,md.medicine.price]
                mst_vaccine_ny.append(a)
            except:
                pass
    
        elif not 'DHPPiL4' in np.array(mst_vaccine_ny):
            try:
                mrt = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='DHPPiL4').values('inventory').annotate(sum=Sum('quantity'))
                inv = 0
                invq = 0
                temp =[]
                for i in mrt: 
                    for key,value in i.items():
                        if key == 'inventory':
                            i = value
                        if key == 'sum':
                            s = value
                            a = [i, s]
                            temp.append(a)

                #medicine inventory, count
                for (n, (item1,item2)) in enumerate(temp):
                    if item2 > invq:
                        inv = item1
                        inv1 = item2

                md = Medicine_Inventory.objects.get(id=inv)
                a = [md,md.medicine.immunization,md.medicine.price]
                mst_vaccine_ny.append(a)
            except:
                pass

        #item, quantity, total
        vac_ny = []


        #3 dhppil_cv, 1 anti rabies, 2 bordertella, 2 dhppil4,
        #3 anti rabies, bordertella, dhppil4,
        
        for (n, (item1, item2, item3)) in enumerate(mst_vaccine_ny):
            if item2 == 'Anti-Rabies':
                mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
                m = Medicine_Inventory.objects.get(id=item1.id)
                c = mi - eny_ar_count
                bn = int((born_ny + k9_ny) - c)
                pr = round(bn*m.medicine.price, 2)
                mi_a = [m,m.medicine.price,bn,pr,int(born_ny + k9_ny)]
                if pr > 0:
                    vac_ny.append(mi_a)
            elif item2 == 'Bordetella Bronchiseptica Bacterin':
                mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
                m = Medicine_Inventory.objects.get(id=item1.id)
                c = mi - eny_bbb_count
                bn = int(((born_ny*2) + k9_ny) - c)
                pr = round(bn*m.medicine.price, 2)
                mi_a = [m,m.medicine.price,bn,pr,int(born_ny + k9_ny)]
                if pr > 0:
                    vac_ny.append(mi_a)
            elif item2 == 'DHPPiL+CV':
                mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
                m = Medicine_Inventory.objects.get(id=item1.id)
                c = mi - eny_dcv_count
                bn = int(((born_ny*3) + k9_ny) - c)
                pr = round(bn*m.medicine.price, 2)
                mi_a = [m,m.medicine.price,bn,pr,int(born_ny + k9_ny)]
                if pr > 0:
                    vac_ny.append(mi_a)
            elif item2 == 'DHPPiL4':
                mi = Medicine_Inventory.objects.filter(medicine__immunization=item2).aggregate(sum=Sum('quantity'))['sum']
                m = Medicine_Inventory.objects.get(id=item1.id)
                c = mi - eny_dc4_count
                bn = int(((born_ny*2) + k9_ny) - c)
                pr = round(bn*m.medicine.price, 2)
                mi_a = [m,m.medicine.price,bn,pr,int(born_ny + k9_ny)]
                if pr > 0:
                    vac_ny.append(mi_a)
        #4 deworming, 8 heartworm, 7 tick&flee

    # Deworming 
        try:
            data = Medicine_Subtracted_Trail.objects.filter(inventory__medicine__immunization='Deworming').values('inventory').annotate(sum=Sum('quantity'))
            print(data)
            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)
        
            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    invq = item2
            print(inv)
            md = Medicine_Inventory.objects.get(id=inv)
            dcq = Medicine_Inventory.objects.filter(medicine__immunization='Deworming').aggregate(sum=Sum('quantity'))['sum']
            dcq = dcq - eny_dw_count
            p_deworm = md.medicine.price
            q_deworm = int((born_ny * 7) + ((k9_ny+need_procure_ny) * 2) - dcq)
            t_deworm = p_deworm*q_deworm
            mi_a = [md,md.medicine.price,q_deworm,t_deworm,int(born_ny+k9_ny+need_procure_ny)]
            if t_deworm > 0:
                vac_ny.append(mi_a)

        except:
            data = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Deworming').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            dcq = Medicine_Inventory.objects.filter(medicine__immunization='Deworming').aggregate(sum=Sum('quantity'))['sum']
            dcq = dcq - eny_dw_count
            p_deworm = md.medicine.price
            q_deworm = int((born_ny * 7) + ((k9_ny+need_procure_ny) * 2) - dcq)
            t_deworm = p_deworm*q_deworm
            mi_a = [md,md.medicine.price,q_deworm,t_deworm,int(born_ny+k9_ny+need_procure_ny)]
            if t_deworm > 0:
                vac_ny.append(mi_a)

        # Heartworm
        try:
            data = Medicine_Subtracted_Trail.objects.filter(inventory__medicine__immunization='Heartworm').values('inventory').annotate(sum=Sum('quantity'))
            
            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            hcq = Medicine_Inventory.objects.filter(medicine__immunization='Heartworm').aggregate(sum=Sum('quantity'))['sum']
            hcq = hcq - eny_hw_count
            p_heatworm = md.medicine.price
            q_heatworm = int((born_ny * 8) + ((k9_ny+need_procure_ny) * 12) - hcq)
            t_heatworm = p_heatworm*q_heatworm
            mi_a = [md,md.medicine.price,q_heatworm,t_heatworm,int(born_ny+k9_ny+need_procure_ny)]
            if t_heatworm > 0:
                vac_ny.append(mi_a)
        except:
            data = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Heartworm').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            hcq = Medicine_Inventory.objects.filter(medicine__immunization='Heartworm').aggregate(sum=Sum('quantity'))['sum']
            hcq = hcq - eny_hw_count
            p_heatworm = md.medicine.price
            q_heatworm = int((born_ny * 8) + ((k9_ny+need_procure_ny) * 12) - hcq)
            t_heatworm = p_heatworm*q_heatworm
            mi_a = [md,md.medicine.price,q_heatworm,t_heatworm,int(born_ny+k9_ny+need_procure_ny)]
            if t_heatworm > 0:
                vac_ny.append(mi_a)

        # Tick & Flee
        try:
            data = Medicine_Subtracted_Trail.objects.filter(inventory__medicine__immunization='Tick and Flea').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            tcq = Medicine_Inventory.objects.filter(medicine__immunization='Tick and Flea').aggregate(sum=Sum('quantity'))['sum']
            tcq = tcq - eny_tf_count
            p_tickflea = md.medicine.price
            k_tf = k9_cy % 7
            q_tickflea = int((born_ny * 7 ) + ((k_tf/k9_cy) * (k9_ny+need_procure_ny)) - tcq)
            t_tickflea = round(Decimal(p_tickflea)*Decimal(q_tickflea), 2)
            mi_a = [md,md.medicine.price,q_tickflea,t_tickflea,int(born_ny+k9_ny+need_procure_ny)]
            if t_tickflea > 0:
                vac_ny.append(mi_a)
        except:
            data = Medicine_Received_Trail.objects.filter(inventory__medicine__immunization='Tick and Flea').values('inventory').annotate(sum=Sum('quantity'))

            inv = 0
            invq = 0
            temp =[]
            for i in data: 
                for key,value in i.items():
                    if key == 'inventory':
                        i = value
                    if key == 'sum':
                        s = value
                        a = [i, s]
                        temp.append(a)

            #medicine inventory, count
            for (n, (item1,item2)) in enumerate(temp):
                if item2 > invq:
                    inv = item1
                    inv1 = item2

            md = Medicine_Inventory.objects.get(id=inv)
            tcq = Medicine_Inventory.objects.filter(medicine__immunization='Tick and Flea').aggregate(sum=Sum('quantity'))['sum']
            tcq = tcq - eny_tf_count
            p_tickflea = md.medicine.price
            k_tf = k9_cy % 7
            q_tickflea = int((born_ny * 7 ) + ((k_tf/k9_cy) * (k9_ny+need_procure_ny)) - tcq)
            t_tickflea = round(Decimal(p_tickflea)*Decimal(q_tickflea), 2)
            mi_a = [md,md.medicine.price,q_tickflea,t_tickflea,int(born_ny+k9_ny+need_procure_ny)]
            if t_tickflea > 0:
                vac_ny.append(mi_a)

        vac_total = 0
        for (n, (item1, item2, item3,item4,item5)) in enumerate(vac_ny):
            vac_total = vac_total + item4
        #Vet Supply
        #item,quantity,total
        vet_arr=[]
        vet_total = 0
        mvi = Miscellaneous_Subtracted_Trail.objects.filter(inventory__misc_type="Vet Supply").filter(date_subtracted__year=current_year).values('inventory').distinct()

        for m in mvi: 
            for key,value in m.items():
                if key == 'inventory':
                    c = Miscellaneous.objects.get(id=value)
                    mvi_i = Miscellaneous_Subtracted_Trail.objects.filter(inventory=c).filter(date_subtracted__year=current_year).aggregate(sum=Sum('quantity'))['sum']
                    tq = int((mvi_i/k9_cy) * (k9_ny+need_procure_ny+born_ny))
                    tp = round(Decimal(tq)*Decimal(c.price), 2)
                    mv = [c,c.price, int(np.ceil(tq)), tp,int(born_ny+k9_ny+need_procure_ny)]
                    vet_total = vet_total+tp
                    vet_arr.append(mv)
        

        #Kennel supplies 
        #item,quantity,total
        ken_arr=[]
        ken_total = 0

        mki = Miscellaneous_Subtracted_Trail.objects.filter(inventory__misc_type="Kennel Supply").filter(date_subtracted__year=current_year).values('inventory').distinct()

        for m in mki: 
            for key,value in m.items():
                if key == 'inventory':
                    c = Miscellaneous.objects.get(id=value)
                    mvi_i = Miscellaneous_Subtracted_Trail.objects.filter(inventory=c).filter(date_subtracted__year=current_year).aggregate(sum=Sum('quantity'))['sum']
                    tq = int((mvi_i/k9_cy) * (k9_ny+need_procure_ny+born_ny))
                    tp = round(Decimal(tq)*Decimal(c.price), 2)
                    mv = [c,c.price, int(np.ceil(tq)), tp,int(born_ny+k9_ny+need_procure_ny)]
                    ken_total = ken_total+tp
                    ken_arr.append(mv)

        #get Others
        oth_arr = []
        oth_total = 0
        moi = Miscellaneous_Subtracted_Trail.objects.filter(inventory__misc_type="Others").filter(date_subtracted__year=current_year).values('inventory').distinct()
        #get all unique inventory and distribute to dogs

        for m in moi: 
            for key,value in m.items():
                if key == 'inventory':
                    c = Miscellaneous.objects.get(id=value)
                    mvi_i = Miscellaneous_Subtracted_Trail.objects.filter(inventory=c).filter(date_subtracted__year=current_year).aggregate(sum=Sum('quantity'))['sum']
                    tq = int((mvi_i/k9_cy) * (k9_ny+need_procure_ny+born_ny))
                    tp = round(Decimal(tq)*Decimal(c.price), 2)
                    mv = [c,c.price, int(np.ceil(tq)), tp,int(born_ny+k9_ny+need_procure_ny)]
                    oth_total = oth_total+tp
                    oth_arr.append(mv)

        #k9 current dog that needs funds for training
        mat_dog = K9.objects.filter(status='Material Dog').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count() + born_ny + need_procure_ny
        k9_current_train = K9.objects.filter(status='Material Dog').exclude(status="Adopted").exclude(status="Dead").exclude(status="Stolen").exclude(status="Lost").count()
        train_count = int(mat_dog)
        train_total = Decimal(mat_dog * 18000)
        
        train_arr = ['K9 Training',18000,mat_dog,train_total]

        grand_total=total_food+vac_total+total_medicine+vet_total+ken_total+oth_total+train_total+total_p
        
    except:
        pass

    context = {
        'total_p':total_p,
        'dog_food':dog_food,
        'total_food':total_food,
        'vac_ny':vac_ny,
        'vac_total':vac_total,
        'b_ny_med': b_ny_med,
        'total_medicine':total_medicine,
        'vet_arr': vet_arr,
        'vet_total': vet_total,
        'ken_arr': ken_arr,
        'ken_total': ken_total,
        'oth_arr': oth_arr,
        'oth_total': oth_total,
        'train_arr':train_arr,
        'train_total':train_total,
        'grand_total': grand_total,
        'stat': stat,
    }

    return render(request, 'planningandacquiring/budget_data.html', context)
