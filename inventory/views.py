from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages

from inventory.models import Medicine, Food, Equipment, Medicine_Inventory, Food_Inventory, Equipment_Inventory
from inventory.models import Medicine_Inventory_Count, Food_Inventory_Count, Equipment_Inventory_Count

from inventory.forms import MedicineForm, FoodForm, EquipmentForm
from inventory.forms import MedicineCountForm, FoodCountForm, EquipementCountForm
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
            
            #save in medicine inventory
            data_id = Medicine.objects.last() 
            Medicine_Inventory.objects.create(medicine = data_id, quantity = 0)

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

def medicine_edit(request, id):
    item = Medicine.objects.get(id=id)
    form = MedicineForm(request.POST or None, instance = item)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../list-medicine')
          
    context = {
        'form': form,
        'title': 'Edit Medicine Form',
        'texthelp': 'Edit Medicine data here',
        'actiontype': 'Submit',
    }
    return render (request, 'inventory/medicine_add.html',context)

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
            
            #save in food inventory
            data_id = Food.objects.last() 
            Food_Inventory.objects.create(food = data_id, quantity = 0)

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

def food_edit(request, id):
    item = Food.objects.get(id=id)
    form = FoodForm(request.POST or None, instance = item)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Dog Food has been successfully Edited!')
            return HttpResponseRedirect('../../list-food')
          
    context = {
        'form': form,
        'title': 'Edit Dog Food Form',
        'texthelp': 'Edit Dog Food data here',
        'actiontype': 'Submit',
    }
    return render (request, 'inventory/food_add.html',context)

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
            
            #save in equipment inventory
            data_id = Equipment.objects.last() 
            Equipment_Inventory.objects.create(equipment = data_id, quantity = 0)

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

def equipment_edit(request, id):
    item = Equipment.objects.get(id=id)
    form = Equipment(request.POST or None, instance = item)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('../../list-equipment')
          
    context = {
        'form': form,
        'title': 'Edit Equipment Form',
        'texthelp': 'Edit Equipment data here',
        'actiontype': 'Submit',
    }
    return render (request, 'inventory/equipment_add.html',context)

def equipment_delete(request, id):
    data = Equipment.objects.get(id=id)
    data.delete()
    messages.success(request, 'Dog Food has been Successfully Deleted!')
    return HttpResponseRedirect('../../list-equipment')

#Inventory
def medicine_inventory_list(request):
    data = Medicine_Inventory.objects.all()
    context = {
        'title': 'Medicine Inventory List',
        'data' : data,
    }
    return render (request, 'inventory/medicine_inventory_list.html',context)

def food_inventory_list(request):
    data = Food_Inventory.objects.all()
    context = {
        'title': 'Dog Food Inventory List',
        'data' : data,
    }
    return render (request, 'inventory/food_inventory_list.html',context)

def equipment_inventory_list(request):
    data = Equipment_Inventory.objects.all()
    context = {
        'title': 'Equipment Inventory List',
        'data' : data,
    }
    return render (request, 'inventory/equipment_inventory_list.html',context)

#Inventory Count List
def medicine_inventory_count(request, id):
    i = Medicine.objects.get(id=id)
    data = Medicine_Inventory_Count.objects.filter(inventory=id).order_by('-time')
    context = {
        'title': i.medicine_fullname,
        'data' : data,
    }
    return render (request, 'inventory/medicine_inventory_count.html', context)

def food_inventory_count(request, id):
    i = Food.objects.get(id=id)
    data = Food_Inventory_Count.objects.filter(inventory=id).order_by('-time')
    context = {
        'title': i.food,
        'data' : data,
    }
    return render (request, 'inventory/food_inventory_count.html', context)

def equipment_inventory_count(request, id):
    i = Equipment.objects.get(id=id)
    data = Equipment_Inventory_Count.objects.filter(inventory=id).order_by('-time')
    context = {
        'title': i.equipment,
        'data' : data,
    }
    return render (request, 'inventory/equipment_inventory_count.html', context)

#Inventory Count Form
#TODO
#ADD USER
def medicine_count_form(request, id):
    data = Medicine_Inventory.objects.get(id=id)
    form = MedicineCountForm(request.POST or None)
    if request.method == 'POST':
      
        #Get session user id
        # user_id = request.session['session_userid']
        # current_user = User.objects.get(id=user_id)

        data.quantity = request.POST.get('quantity')
        data.save()
        #TODO 
        # add user = current_user
        Medicine_Inventory_Count.objects.create(inventory = data, quantity = request.POST.get('quantity'))
        return redirect('inventory:medicine_inventory_count', id = data.id)
            
    context = {
        'title': data.medicine,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
    }
    return render (request, 'inventory/medicine_count_form.html', context)

#TODO
#ADD USER
def food_count_form(request, id):
    data = Food_Inventory.objects.get(id=id)
    form = FoodCountForm(request.POST or None)
    if request.method == 'POST':
      
        #Get session user id
        # user_id = request.session['session_userid']
        # current_user = User.objects.get(id=user_id)

        data.quantity = request.POST.get('quantity')
        data.save()
        #TODO 
        # add user = current_user
        Food_Inventory_Count.objects.create(inventory = data, quantity = request.POST.get('quantity'))
        return redirect('inventory:food_inventory_count', id = data.id)
            
    context = {
        'title': data.food,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
    }
    return render (request, 'inventory/food_count_form.html', context)

#TODO
#ADD USER
def equipment_count_form(request, id):
    data = Equipment_Inventory.objects.get(id=id)
    form = EquipementCountForm(request.POST or None)
    if request.method == 'POST':
      
        #Get session user id
        # user_id = request.session['session_userid']
        # current_user = User.objects.get(id=user_id)

        data.quantity = request.POST.get('quantity')
        data.save()
        #TODO 
        # add user = current_user
        Equipment_Inventory_Count.objects.create(inventory = data, quantity = request.POST.get('quantity'))
        return redirect('inventory:equipment_inventory_count', id = data.id)
            
    context = {
        'title': data.equipment,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
    }
    return render (request, 'inventory/equipment_count_form.html', context)