from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages

from planningandacquiring.models import K9
from unitmanagement.models import PhysicalExam, Health, HealthMedicine
from unitmanagement.forms import PhysicalExamForm, HealthForm, HealthMedicineForm
from inventory.models import Medicine
from unitmanagement.models import HealthMedicine, Health
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

#TODO
#FIX THIS as well as Health_forms.html
def health_form(request):
    medicine_formset = inlineformset_factory(Health, HealthMedicine, form=HealthMedicineForm, extra=1, can_delete=True)
    form = HealthForm(request.POST or None)
    if request.method == "POST":
        print(form)
        if form.is_valid():
            new_form = form.save()
            new_form = new_form.pk
            form_instance = PurchaseRequisition.objects.get(id=new_form)

            #Use Health form instance for Health Medicine
            formset = medicine_formset(request.POST, instance=form_instance)
            print(formset)
            if formset.is_valid():
                for form in formset:
                    form.save()
           
    context = {
        'title': "Health Form",
        'form':HealthForm,
        'formset':medicine_formset(),
        'actiontype': "Submit",
    }
    return render (request, 'unitmanagement/health_form.html', context)

def physical_exam_form(request):
    form = PhysicalExamForm(request.POST or None)
    form.fields["dog"].queryset = K9.objects.all().order_by('name')

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
    }
    return render (request, 'unitmanagement/physical_exam_form.html', context)

def health_record(request):
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
    context = {
        'title': "Health History of ",
        'name': data.name,
        'actiontype': "Submit",
        'data': data,
        'health_data': health_data, 
        'phyexam_data': phyexam_data, 
    }
    return render (request, 'unitmanagement/health_history.html', context)

def health_details(request, id):
    data = Health.objects.get(id=id)
    medicine = HealthMedicine.objects.filter(health=data)
    dog = K9.objects.get(id = data.dog.id)
    context = {
        'title': "Health Details of ",
        'name': dog.name,
        'data': data,
        'medicine': medicine,
        'dog': dog,
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