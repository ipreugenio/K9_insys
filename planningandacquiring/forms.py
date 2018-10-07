from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from .models import K9

class DateInput(forms.DateInput):
    input_type = 'date'

class add_K9_form(forms.ModelForm):
    SOURCE = (
        ('Breeding', 'Breeding'),
        ('Donation', 'Donation'),
    )

    source = forms.CharField(max_length=50, label = 'source', widget = forms.Select(choices=SOURCE))
    class Meta:
        model = K9
        fields = ('serial_number', 'name', 'breed', 'sex', 'color', 'birth_date', 'microchip', 'source')

        widgets = {
            'birth_date': DateInput(),
        }