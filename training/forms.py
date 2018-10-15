from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from planningandacquiring.models import K9

class DateInput(forms.DateInput):
    input_type = 'date'

class TestForm(forms.Form):
    k9 = forms.ModelChoiceField(queryset=K9.objects.all())