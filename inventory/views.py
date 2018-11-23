from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
import datetime
from django.contrib.sessions.models import Session
from profiles.models import User, Account
from inventory.models import Medicine, Food, Miscellaneous, Medicine_Inventory, Food_Inventory, Miscellaneous_Inventory
from inventory.models import Medicine_Inventory_Count, Food_Inventory_Count, Miscellaneous_Inventory_Count
from inventory.models import Medicine_Received_Trail, Food_Received_Trail, Miscellaneous_Received_Trail, DamagedEquipemnt
from inventory.models import Medicine_Subtracted_Trail, Food_Subtracted_Trail, Miscellaneous_Subtracted_Trail

from inventory.forms import MedicineForm, FoodForm, MiscellaneousForm, DamagedEquipmentForm
from inventory.forms import MedicineCountForm, FoodCountForm, MiscellaneousCountForm
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
        'title': 'Medicine Form',
        'texthelp': 'Input Medicine data here',
        'actiontype': 'Submit',
        'style' : style,
    }
    return render (request, 'inventory/medicine_add.html',context)

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
        'title': 'Dog Food Form',
        'texthelp': 'Input Dog food data here',
        'actiontype': 'Submit',
        'style' : style,
    }
    return render (request, 'inventory/food_add.html', context)

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

#Miscellaneous
def miscellaneous_add(request):
    form = MiscellaneousForm(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        print(form.errors)
        if form.is_valid():
            form.save()
            
            #save in miscellaneous inventory
            data_id = Miscellaneous.objects.last() 
            Miscellaneous_Inventory.objects.create(miscellaneous = data_id, quantity = 0)

            style = "ui green message"
            messages.success(request, 'Miscellaneous Item has been successfully Added!')
            form = MiscellaneousForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'form': form,
        'title': 'Miscellaneous Item Form',
        'texthelp': 'Input Miscellaneous data here',
        'actiontype': 'Submit',
        'style' : style,
    }
    return render (request, 'inventory/miscellaneous_add.html', context)

def miscellaneous_edit(request, id):
    item = Miscellaneous.objects.get(id=id)
    form = MiscellaneousForm(request.POST or None, instance = item)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Miscellaneous Item has been successfully Edited!')
            return HttpResponseRedirect('../../list-miscellaneous')
          
    context = {
        'form': form,
        'title': 'Edit Miscellaneous Form',
        'texthelp': 'Edit Miscellaneous data here',
        'actiontype': 'Submit',
    }
    return render (request, 'inventory/miscellaneous_add.html',context)

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

def miscellaneous_inventory_list(request):
    data = Miscellaneous_Inventory.objects.all()
    context = {
        'title': 'Miscellaneous Inventory List',
        'data' : data,
    }
    return render (request, 'inventory/miscellaneous_inventory_list.html',context)

#Inventory Details
def medicine_inventory_details(request, id):
    i = Medicine.objects.get(id=id)
    data = Medicine_Inventory_Count.objects.filter(inventory=id).order_by('-date_counted').order_by('-time')
    data2 = Medicine_Received_Trail.objects.filter(inventory=id).order_by('-date_received').order_by('-time')
    data3 = Medicine_Subtracted_Trail.objects.filter(inventory=id).order_by('-date_subtracted').order_by('-time')
    form = MedicineForm(request.POST or None, instance = i)
    style=""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Medicine has been successfully Updated!')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    context = {
        'title': i.medicine_fullname,
        'data' : data,
        'data2': data2,
        'data3': data3,
        'form': form,
        'actiontype': 'Update',
        'style': style,
    }
    return render (request, 'inventory/medicine_inventory_details.html', context)

def food_inventory_details(request, id):
    i = Food.objects.get(id=id)
    data = Food_Inventory_Count.objects.filter(inventory=id).order_by('-date_counted').order_by('-time')
    data2 = Food_Received_Trail.objects.filter(inventory=id).order_by('-date_received').order_by('-time')
    data3 = Food_Subtracted_Trail.objects.filter(inventory=id).order_by('-date_subtracted').order_by('-time')
    form = FoodForm(request.POST or None, instance = i)
    style=""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Dog Food has been successfully Updated!')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    context = {
        'title': i.food,
        'data' : data,
        'data2': data2,
        'data3': data3,
        'form': form,
        'actiontype': 'Update',
        'style': style,
    }
    return render (request, 'inventory/food_inventory_details.html', context)

def miscellaneous_inventory_details(request, id):
    i = Miscellaneous.objects.get(id=id)
    data = Miscellaneous_Inventory_Count.objects.filter(inventory=id).order_by('-date_counted').order_by('-time')
    data2 = Miscellaneous_Received_Trail.objects.filter(inventory=id).order_by('-date_received').order_by('-time')
    data3 = Miscellaneous_Subtracted_Trail.objects.filter(inventory=id).order_by('-date_subtracted').order_by('-time')
    form = MiscellaneousForm(request.POST or None, instance = i)
    style=""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Miscellaneous Item has been successfully Updated!')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    context = {
        'title': i.miscellaneous,
        'data' : data,
        'data2': data2,
        'data3': data3,
        'form': form,
        'actiontype': 'Update',
        'style': style,
    }
    return render (request, 'inventory/miscellaneous_inventory_details.html', context)

#Inventory Count Form
#TODO
#ADD USER
def medicine_count_form(request, id):
    data = Medicine_Inventory.objects.get(id=id)
    form = MedicineCountForm(request.POST or None)
    style = ""

    if request.method == 'POST':
        if form.is_valid():
            #Get session user id
            user_serial = request.session['session_serial']
            user = Account.objects.filter(serial_number = user_serial)
            current_user = User.objects.get(id=user.id)

            data.quantity = request.POST.get('quantity')
            data.save()
            #TODO 
            # add user = current_user
            Medicine_Inventory_Count.objects.create(inventory = data, user = current_user, quantity = request.POST.get('quantity'), date_counted = datetime.date.today(), time = datetime.datetime.now())
            style = "ui green message"
            form = MedicineCountForm()
            messages.success(request, 'Medicine has been successfully Updated!')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
        
        return HttpResponseRedirect('../../list-medicine-inventory')
            
    context = {
        'title': data.medicine,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
        'label': 'Physical Count',
        'style':style,
        'texthelp': 'Input Medicine Physical Count data here',
    }
    return render (request, 'inventory/medicine_count_form.html', context)

#TODO
#ADD USER
def food_count_form(request, id):
    data = Food_Inventory.objects.get(id=id)
    form = FoodCountForm(request.POST or None)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            #Get session user id
            user_serial = request.session['session_serial']
            user = Account.objects.filter(serial_number = user_serial)
            current_user = User.objects.get(id=user.id)

            data.quantity = request.POST.get('quantity')
            data.save()
            #TODO 
            # add user = current_user
            Food_Inventory_Count.objects.create(inventory = data, quantity = request.POST.get('quantity'), user = current_user, date_counted = datetime.date.today(), time = datetime.datetime.now())
            style = "ui green message"
            form = FoodCountForm()
            messages.success(request, 'Dog Food has been successfully Updated!')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
        
        return HttpResponseRedirect('../../list-food-inventory')
            
    context = {
        'title': data.food,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
        'label': 'Physical Count',
        'style':style,
        'texthelp': 'Input Dog Food Physical Count here',
    }
    return render (request, 'inventory/food_count_form.html', context)

#TODO
#ADD USER
def miscellaneous_count_form(request, id):
    data = Miscellaneous_Inventory.objects.get(id=id)
    form = MiscellaneousCountForm(request.POST or None)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            #Get session user id
             user_serial = request.session['session_serial']
            user = Account.objects.filter(serial_number = user_serial)
            current_user = User.objects.get(id=user.id)

            data.quantity = request.POST.get('quantity')
            data.save()
            #TODO 
            # add user = current_user
            Miscellaneous_Inventory_Count.objects.create(inventory = data, user = current_user, quantity = request.POST.get('quantity'), date_counted = datetime.date.today(), time = datetime.datetime.now())
            style = "ui green message"
            form = MiscellaneousCountForm()
            messages.success(request, 'Miscellaneous Item has been successfully Updated!')
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
        
        return HttpResponseRedirect('../../list-miscellaneous-inventory')
            
    context = {
        'title': data.miscellaneous,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
        'label': 'Physical Count',
        'texthelp': 'Input Miscellaneous Physical Count here',
    }
    return render (request, 'inventory/miscellaneous_count_form.html', context)

#Inventory add quantity
def medicine_receive_form(request, id):
    data = Medicine_Inventory.objects.get(id=id)
    form = MedicineCountForm(request.POST or None)
    style=""
    if request.method == 'POST':
        if form.is_valid():
            current_quantity = data.quantity
            data.quantity = int(current_quantity) + int(request.POST.get('quantity'))
            data.save()
    
            style = "ui green message"
            form = MedicineCountForm()
            messages.success(request, 'Medicine has been successfully Updated!')
            
            user_serial = request.session['session_serial']
            user = Account.objects.filter(serial_number = user_serial)
            current_user = User.objects.get(id=user.id)

            Medicine_Received_Trail.objects.create(inventory = data, user = current_user, quantity = request.POST.get('quantity'), date_received = datetime.date.today(), time = datetime.datetime.now())

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

        return HttpResponseRedirect('../../list-medicine-inventory')

    context = {
        'title': data.medicine,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
        'label': 'No. of Received Items ',
        'style': style,
        'texthelp': 'Input Received Medicine Quantity here',
    }
    return render (request, 'inventory/medicine_count_form.html', context)

def food_receive_form(request, id):
    data = Food_Inventory.objects.get(id=id)
    form = FoodCountForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_quantity = data.quantity
            data.quantity = int(current_quantity) + int(request.POST.get('quantity'))
            data.save()
            style = "ui green message"
            messages.success(request, 'Food has been successfully Updated!')
            form = FoodCountForm()
             
            user_serial = request.session['session_serial']
            user = Account.objects.filter(serial_number = user_serial)
            current_user = User.objects.get(id=user.id)

            Food_Received_Trail.objects.create(inventory = data, user = current_user, quantity = request.POST.get('quantity'), date_received = datetime.date.today(), time = datetime.datetime.now())
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
        
        return HttpResponseRedirect('../../list-food-inventory')

    context = {
        'title': data.food,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
        'label': 'Kg. of Received Items ',
        'texthelp': 'Input Received Dog Food Quantity here',
    }
    return render (request, 'inventory/food_count_form.html', context)

def miscellaneous_receive_form(request, id):
    data = Miscellaneous_Inventory.objects.get(id=id)
    form = MiscellaneousCountForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_quantity = data.quantity
            data.quantity = int(current_quantity) + int(request.POST.get('quantity'))
            data.save()
            style = "ui green message"
            messages.success(request, 'Miscellaneous Item has been successfully Updated!')
            form = MiscellaneousCountForm()
             
            user_serial = request.session['session_serial']
            user = Account.objects.filter(serial_number = user_serial)
            current_user = User.objects.get(id=user.id)

            Miscellaneous_Received_Trail.objects.create(inventory = data, user = 'current_user', quantity = request.POST.get('quantity'), date_received = datetime.date.today(), time = datetime.datetime.now())
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
        
        return HttpResponseRedirect('../../list-miscellaneous-inventory')

    context = {
        'title': data.miscellaneous,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
        'label': 'No. of Received Items',
        'texthelp': 'Input Received Miscellaneous Items Quantity here',
    }
    return render (request, 'inventory/miscellaneous_count_form.html', context)

#Inventory subtract quantity
def medicine_subtract_form(request, id):
    data = Medicine_Inventory.objects.get(id=id)
    form = MedicineCountForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_quantity = data.quantity
            data.quantity = int(current_quantity) - int(request.POST.get('quantity'))
            data.save()
            style = "ui green message"
            messages.success(request, 'Medicine has been successfully Updated!')
            form = MedicineCountForm()
            
            user_serial = request.session['session_serial']
            user = Account.objects.filter(serial_number = user_serial)
            current_user = User.objects.get(id=user.id)
            
            Medicine_Subtracted_Trail.objects.create(inventory = data, user=current_user, quantity = request.POST.get('quantity'), date_subtracted = datetime.date.today(), time = datetime.datetime.now())
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
        
        return HttpResponseRedirect('../../list-medicine-inventory')

    context = {
        'title': data.medicine,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
        'label': 'No. of Medicine Items Subtracted',
        'texthelp': 'Input Subtracted Medicine Quantity here',
    }
    return render (request, 'inventory/medicine_count_form.html', context)

def food_subtract_form(request, id):
    data = Food_Inventory.objects.get(id=id)
    form = FoodCountForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_quantity = data.quantity
            data.quantity = int(current_quantity) - int(request.POST.get('quantity'))
            data.save()
            style = "ui green message"
            messages.success(request, 'Food has been successfully Updated!')
            form = FoodCountForm()

            user_serial = request.session['session_serial']
            user = Account.objects.filter(serial_number = user_serial)
            current_user = User.objects.get(id=user.id)

            Food_Subtracted_Trail.objects.create(inventory = data, user=current_user, quantity = request.POST.get('quantity'), date_subtracted = datetime.date.today(), time = datetime.datetime.now())
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
        
        return HttpResponseRedirect('../../list-food-inventory')

    context = {
        'title': data.food,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
        'label': 'Kg. of Food Subtracted',
        'texthelp': 'Input Subtracted Dog Food Quantity here',
    }
    return render (request, 'inventory/food_count_form.html', context)

def miscellaneous_subtract_form(request, id):
    data = Miscellaneous_Inventory.objects.get(id=id)
    form = MiscellaneousCountForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            current_quantity = data.quantity
            data.quantity = int(current_quantity) - int(request.POST.get('quantity'))
            data.save()
            style = "ui green message"
            messages.success(request, 'Miscellaneous Item has been successfully Updated!')
            form = MiscellaneousCountForm()

            user_serial = request.session['session_serial']
            user = Account.objects.filter(serial_number = user_serial)
            current_user = User.objects.get(id=user.id)

            Miscellaneous_Subtracted_Trail.objects.create(inventory = data, user = current_user, quantity = request.POST.get('quantity'), date_subtracted = datetime.date.today(), time = datetime.datetime.now())
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
        
        return HttpResponseRedirect('../../list-miscellaneous-inventory')

    context = {
        'title': data.miscellaneous,
        'form': form,
        'data' : data,
        'actiontype': 'Submit',
        'label': 'No. of Items Subtracted',
        'texthelp': 'Input Subtracted Miscellaneous Items Quantity here',
    }
    return render (request, 'inventory/miscellaneous_count_form.html', context)

#Damaged Form
def damaged_form(request):
    form = DamagedEquipmentForm(request.POST or None)
    style = ""
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            style = "ui green message"
            messages.success(request, 'Equipment has been successfully Reported!')
            form = DamagedEquipmentForm()
        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')
    context = {
        'title': 'Report Equipment Concern',
        'form' : form,
        'style':style,
    }
    return render (request, 'inventory/damaged_form.html',context)
    
def damaged_report_list(request):
    data = DamagedEquipemnt.objects.all()
    
    context = {
        'title': 'Report Damaged Equipment List',
        'data' : data,
    }
    return render (request, 'inventory/damaged_report_list.html',context)