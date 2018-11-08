from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from planningandacquiring.models import K9
from training.models import K9_Handler

class DateInput(forms.DateInput):
    input_type = 'date'

class TestForm(forms.Form):
    k9 = forms.ModelChoiceField(queryset=K9.objects.all())

class add_handler_form(forms.ModelForm):
    class Meta:
        model = K9_Handler
        fields = ('handler', 'k9')

    def __init__(self, *args, **kwargs):
        super(add_handler_form, self).__init__(*args, **kwargs)
        self.fields['handler'].queryset = self.fields['handler'].queryset.exclude(position="Veterinarian")
        self.fields['handler'].queryset = self.fields['handler'].queryset.exclude(position="Administrator")
        assigned_handler = K9_Handler.objects.all()
        assigned_handler_list = []
        for handler in assigned_handler:
            assigned_handler_list.append(handler.id)
        self.fields['handler'].queryset = self.fields['handler'].queryset.exclude(pk__in=assigned_handler_list)
