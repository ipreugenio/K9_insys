from django.shortcuts import render
from .forms import add_K9_form
from .models import K9
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, inlineformset_factory
from django.db.models import aggregates
from django.contrib import messages
# Create your views here.

# Create your views here.

def index(request):
    return render (request, 'planningandacquiring/index.html')

#Form format
def add_K9(request):
    form = add_K9_form(request.POST)
    style = "ui teal message"
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            style = "ui green message"
            messages.success(request, 'K9 has been successfully Added!')
            form = add_K9_form()

        else:
            style = "ui red message"
            messages.warning(request, 'Invalid input data!')

    context = {
        'Title' : "Add K9",
        'form' : add_K9_form,
        'style': style,
            }

    return render(request, 'planningandacquiring/add_K9.html', context)

#Listview format
def K9_listview(request):
    k9 = K9.objects.all()
    context = {
        'Title' : 'K9 List',
        'k9' : k9
    }

    return render(request, 'planningandacquiring/K9_list.html', context)

#Detailview format
def K9_detailview(request, id):
    k9 = K9.objects.get(id = id)
    context = {
        'Title': 'K9 Details',
        'k9' : k9
    }

    return render(request, 'planningandacquiring/K9_detail.html', context)

'''
def delete_K9(request, id):
    k9 = K9.objects.get(id=id)
'''