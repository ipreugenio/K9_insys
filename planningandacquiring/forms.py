from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from .models import K9, K9_Past_Owner, K9_Parent

class DateInput(forms.DateInput):
    input_type = 'date'

class add_donated_K9_form(forms.ModelForm):
    class Meta:
        model = K9
        fields = ('name', 'breed', 'sex', 'color', 'birth_date')
        widgets = {
            'birth_date': DateInput(),
        }

class add_donator_form(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = K9_Past_Owner
        fields = ('first_name', 'middle_name', 'last_name', 'email', 'contact_no', 'address')

class add_K9_parents_form(forms.ModelForm):
    class Meta:
        model = K9_Parent
        fields = ('mother', 'father', 'offspring')

    def __init__(self, *args, **kwargs):
        super(add_K9_parents_form, self).__init__(*args, **kwargs)
        self.fields['mother'].queryset = self.fields['mother'].queryset.exclude(sex="M")
        self.fields['father'].queryset = self.fields['father'].queryset.exclude(sex="F")

class add_offspring_K9_form(forms.ModelForm):
    class Meta:
        model = K9
        fields = ('name', 'breed', 'sex', 'color', 'birth_date')
        widgets = {
            'birth_date': DateInput(),
        }