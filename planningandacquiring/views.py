from django.shortcuts import render
from .forms import add_K9_form
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
    if request.method == 'POST':
        if form.is_valid():
            form.save()

    context = {
        'form' : add_K9_form
            }

    return render(request, 'planningandacquiring/add_K9.html', context)
