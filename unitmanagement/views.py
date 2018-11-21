from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
import datetime as dt

from planningandacquiring.models import K9
from unitmanagement.models import PhysicalExam, Health, HealthMedicine
from unitmanagement.forms import PhysicalExamForm, HealthForm, HealthMedicineForm, VaccinationForm, RequestForm
from inventory.models import Medicine, Medicine_Inventory, Medicine_Subtracted_Trail
from unitmanagement.models import HealthMedicine, Health, VaccinceRecord, Requests
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
    data = K9.objects.get(id=id)
    health_data = Health.objects.filter(dog = data)
    phyexam_data = PhysicalExam.objects.filter(dog = data)
    vaccine_data = VaccinceRecord.objects.filter(dog = data)
    context = {
        'title': "Health History of ",
        'name': data.name,
        'actiontype': "Submit",
        'data': data,
        'health_data': health_data,
        'phyexam_data': phyexam_data,
        'vaccine_data': vaccine_data,
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

    if medicine.count() == count:
        for med in medicine:
            i = Medicine_Inventory.objects.filter(id = med.medicine.id) # get Inventory Items
            for x in i:
                Medicine_Subtracted_Trail.objects.create(inventory = x, quantity = med.quantity, date_subtracted = datetime.date.today(), time = datetime.datetime.now())
                x.quantity = (x.quantity - med.quantity)
                data.status = "Approved"
                data.save()
                x.save()

        messages.success(request, 'Medicine Acquisition has been approved!')
    else:
        messages.warning(request, 'Insufficient Inventory!')
        return redirect('unitmanagement:health_details', id = data.id)

    return redirect('unitmanagement:health_details', id = data.id)

#Vaccination form
def vaccination_form(request):
    form = VaccinationForm(request.POST or None)
    style=""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Vaccination has been successfully recorded!')
            form = VaccinationForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    context = {
        'title': "Vaccination",
        'actiontype': "Submit",
        'form': form,
    }
    return render (request, 'unitmanagement/vaccination_form.html', context)

def requests_form(request):
    form = RequestForm(request.POST or None)
    style=""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
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
    if request.method == 'POST':
        if 'ok' in request.POST:
            data.request_status = "Approved"
            data.date_approved = changedate
            data.save()
            style = "ui green message"
            messages.success(request, 'Equipment Approved!')
        else:
            data.request_status = "Cancelled"
            data.date_approved = changedate
            data.save()
            style = "ui red message"
            messages.success(request, 'Equipment Denied!')

    context = {
        'data': data,
        'style': style,
    }

    return render (request, 'unitmanagement/change_equipment.html', context)
