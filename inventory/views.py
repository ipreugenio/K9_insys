from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages

from inventory.models import Medicine, Food, Equipment

from inventory.forms import MedicineForm, FoodForm, EquipmentForm
# Create your views here.

def index(request):
    return render (request, 'inventory/index.html')

#Medicine
def medicine_add(request):
    form = MedicineForm(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Medicine has been successfully Added!')
            form = MedicineForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'form': form,
        'title': 'Add Medicine Form',
        'texthelp': 'Input Medicine data here',
        'actiontype': 'Submit',
        'style' : style,
    }
    return render (request, 'inventory/medicine_add.html',context)

def medicine_list(request):
    data = Medicine.objects.all()
    context = {
        'title': 'Medicine List',
        'data' : data,
    }
    return render (request, 'inventory/medicine_list.html', context)

def medicine_delete(request, id):
    data = Medicine.objects.get(id=id)
    data.delete()
    messages.success(request, 'Dog Food has been Successfully Deleted!')
    return HttpResponseRedirect('../../list-medicine')


#Food
def food_add(request):
    form = FoodForm(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Dog Food has been successfully Added!')
            form = FoodForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'form': form,
        'title': 'Add Dog Food Form',
        'texthelp': 'Input Dog food data here',
        'actiontype': 'Submit',
        'style' : style,
    }
    return render (request, 'inventory/food_add.html', context)


def food_list(request):
    data = Food.objects.all()
    context = {
        'title': 'Food List',
        'data' : data,
    }
    return render (request, 'inventory/food_list.html', context)

def food_delete(request, id):
    data = Food.objects.get(id=id)
    data.delete()
    messages.success(request, 'Dog Food has been Successfully Deleted!')
    return HttpResponseRedirect('../../list-food')

#Equipemnt
def equipment_add(request):
    form = EquipmentForm(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Equipment has been successfully Added!')
            form = EquipmentForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'form': form,
        'title': 'Add Equipment Form',
        'texthelp': 'Input Equipment data here',
        'actiontype': 'Submit',
        'style' : style,
    }
    return render (request, 'inventory/equipment_add.html', context)

def equipment_list(request):
    data = Equipment.objects.all()
    context = {
        'title': 'Equipment List',
        'data' : data,
    }
    return render (request, 'inventory/equipment_list.html', context)

def equipment_delete(request, id):
    data = Equipment.objects.get(id=id)
    data.delete()
    messages.success(request, 'Dog Food has been Successfully Deleted!')
    return HttpResponseRedirect('../../list-equipment')