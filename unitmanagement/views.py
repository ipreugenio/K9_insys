from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
import datetime as dt

from planningandacquiring.models import K9
from unitmanagement.models import PhysicalExam, Health, HealthMedicine, K9_Incident, Handler_Incident
from unitmanagement.forms import PhysicalExamForm, HealthForm, HealthMedicineForm, VaccinationRecordForm, RequestForm
from unitmanagement.forms import K9IncidentForm, HandlerIncidentForm, VaccinationUsedForm, ReassignAssetsForm
from inventory.models import Medicine, Medicine_Inventory, Medicine_Subtracted_Trail, Miscellaneous_Inventory, Miscellaneous_Subtracted_Trail
from unitmanagement.models import HealthMedicine, Health, VaccinceRecord, Requests, VaccineUsed
from profiles.models import User, Account
from training.models import K9_Handler
# Create your views here.

def index(request):
    data = Medicine.objects.all()
    form = HealthMedicineForm(request.POST or None)
    res = ""
    med_id = ""
    if request.method == "POST":
        res = request.POST.get('dropdown')
        med_id = Medicine.objects.get(id=res)
        hm = Health.objects.last()
        HealthMedicine.objects.create(health = hm, medicine_id = med_id.id,
        medicine = med_id.medicine_fullname, quantity = 10, dosage = "take 3x a day")
        form = HealthMedicineForm()
    context = {
        'title': "Unit Management Test Page",
        'data': data,
        'form': form,
    }
    return render (request, 'unitmanagement/index.html', context)

#TODO Formset does not got to db
#FIX THIS as well as Health_forms.html
def health_form(request):
    medicine_formset = inlineformset_factory(Health, HealthMedicine, form=HealthMedicineForm, extra=1, can_delete=True)
    form = HealthForm(request.POST or None)
    style=""
    if request.method == "POST":
        print(form)
        if form.is_valid():
            new_form = form.save()
            new_form = new_form.pk
            form_instance = Health.objects.get(id=new_form)

            #Use Health form instance for Health Medicine
            formset = medicine_formset(request.POST, instance=form_instance)

            print(formset)
            if formset.is_valid():
                for form in formset:
                    form.save()
                style = "ui green message"
                messages.success(request, 'Health Form has been successfully recorded!')
            else:
                style = "ui red message"
                messages.warning(request, 'Invalid input data!')

    context = {
        'title': "Health Form",
        'form':HealthForm,
        'formset':medicine_formset(),
        'actiontype': "Submit",
        'style': style,
    }
    return render (request, 'unitmanagement/health_form.html', context)

def physical_exam_form(request):
    form = PhysicalExamForm(request.POST or None)
    form.fields["dog"].queryset = K9.objects.all().order_by('name')
    style=""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            new_form = form.save()
            new_form.date_next_exam = dt.date.today() + dt.timedelta(days=365)

            user_serial = request.session['session_serial']
            user = Account.objects.get(serial_number=user_serial)
            current_user = User.objects.get(id=user.UserID.id)
           
            new_form.user = current_user
            new_form.save()

            style = "ui green message"
            messages.success(request, 'Physical Exam has been successfully recorded!')
            form = PhysicalExamForm()

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    context = {
        'title': "Physical Exam",
        'actiontype': "Submit",
        'form': form,
        'style': style,
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

    context = {
        'title': "Health Record",
        'actiontype': "Submit",
        'data': data,
    }
    return render (request, 'unitmanagement/health_record.html', context)

def health_history(request, id):
    user_serial = request.session['session_serial']
    user = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user.UserID.id)


    data = K9.objects.get(id=id)
    health_data = Health.objects.filter(dog = data)
    phyexam_data = PhysicalExam.objects.filter(dog = data)
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

    #data of vaccines used
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

    }
    return render (request, 'unitmanagement/health_history.html', context)

def health_details(request, id):
    data = Health.objects.get(id=id)
    medicine = HealthMedicine.objects.filter(health=data)
    dog = K9.objects.get(id = data.dog.id)
    count = 0
    style = "ui red message"

    for med in medicine:
        i = Medicine_Inventory.objects.filter(id = med.medicine.id)# get Inventory Items
        for x in i:
            if x.quantity >= med.quantity:
                count = count+1

    if medicine.count() == count:
        style = "ui green message"
    else:
        style = "ui red message"

    context = {
        'title': "Health Details of ",
        'name': dog.name,
        'data': data,
        'medicine': medicine,
        'dog': dog,
        'style':style,
    }
    return render (request, 'unitmanagement/health_details.html', context)

def physical_exam_details(request, id):
    data = PhysicalExam.objects.get(id=id)
    dog = K9.objects.get(id = data.dog.id)
    context = {
        'title': "Physical Exam Details of",
        'name': dog.name,
        'data': data,
        'dog': dog,
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
    form = VaccinationForm(request.POST or None)
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
                form = VaccinationForm()
            else:
                style = "ui red message"
                messages.warning(request, 'Insufficient Inventory Quantity!')
    context = {
        'title': "Vaccination",
        'actiontype': "Submit",
        'form': form,
        'style': style,
    }
    return render (request, 'unitmanagement/vaccination_form.html', context)

def requests_form(request):
    form = RequestForm(request.POST or None)
    style=""

    user_serial = request.session['session_serial']
    user = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user.UserID.id)


    if request.method == 'POST':
        if form.is_valid():
            form.save()
            no_id = form.save()
            no_id.handler = current_user
            no_id.save()

            style = "ui green message"
            messages.success(request, 'Request has been successfully recorded!')
            form = RequestForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    context = {
        'title': "Request of equipment",
        'actiontype': "Submit",
        'style': style,
        'form': form,
    }
    return render (request, 'unitmanagement/request_form.html', context)

def request_list(request):
    data = Requests.objects.all()

    context = {
        'data': data,
        'title': 'Damaged Equipment List',
    }
    return render (request, 'unitmanagement/request_list.html', context)

def change_equipment(request, id):
    data = Requests.objects.get(id=id)
    style = ""
    changedate = dt.datetime.now()

    user_serial = request.session['session_serial']
    user = Account.objects.get(serial_number=user_serial)
    current_user = User.objects.get(id=user.UserID.id)

    if request.method == 'POST':
        if 'ok' in request.POST:
            data.request_status = "Approved"
            data.date_approved = changedate
            data.save()
            #subtract inventory
            equipment = Miscellaneous_Inventory.objects.get(miscellaneous=data.equipment)
            if equipment.quantity > 0:
                equipment.quantity = equipment.quantity-1
                equipment.save()

                Miscellaneous_Subtracted_Trail.objects.create(inventory=equipment, user=current_user,
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

    context = {
        'data': data,
        'style': style,
    }

    return render (request, 'unitmanagement/change_equipment.html', context)

# TODO
# Integrate K9_Handler Model
# MAYBE SOMETHING!! LOOK AT THE CODES OF THE MODEL 
def k9_incident(request):
    form = K9IncidentForm(request.POST or None)
    style=''
    if request.method == "POST":
        if form.is_valid():
            incident_save = form.save()

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
            else:
                k9_obj.status = 'Dead'
                k9_obj.save()

            form = K9IncidentForm()
            style = "ui green message"
            messages.success(request, 'Incident has been successfully Reported!')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    
    context = {
        'title': "K9 Incident",
        'actiontype': "Submit",
        'form': form,
        'style': style,
    }
    return render (request, 'unitmanagement/k9_incident.html', context)

# TODO
# Integrate K9_Handler Model
# MAYBE SOMETHING!! LOOK AT THE CODES OF THE MODEL   
def handler_incident(request):
    form = HandlerIncidentForm(request.POST or None)
    style=''
    if request.method == "POST":
        if form.is_valid():
            incident_save = form.save()

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

    context = {
        'title': "Handler Incident",
        'actiontype': "Submit",
        'form': form,
        'style': style,
    }
    return render (request, 'unitmanagement/handler_incident.html', context)

# TODO
# Integrate K9_Handler Model
# MAYBE SOMETHING!! LOOK AT THE CODES OF THE MODEL   
def reassign_assets(request):
    style=''
    form = ReassignAssetsForm(request.POST or None)
    
    if request.method == 'POST':
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
    context = {
        'title': "Reassign Assets",
        'actiontype': "Submit",
        'style': style,
        'form': form,
    }
    return render (request, 'unitmanagement/reassign_assets.html', context)