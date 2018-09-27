from django.shortcuts import render
from .forms import add_K9_form

# Create your views here.

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