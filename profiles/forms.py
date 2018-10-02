from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from .models import Users

class DateInput(forms.DateInput):
    input_type = 'date'

class add_User_form(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('serial_number', 'firstname', 'lastname', 'nickname', 'position', 'rank', 'extensionname', 'middlename',
                  'gender', 'birthdate', 'birthplace', 'civilstatus', 'citizenship', 'religion', 'bloodtype',
                  'distinct_feature', 'haircolor', 'eyecolor', 'skincolor', 'height', 'weight',
                  'headsize', 'footsize', 'bodybuild')
        widgets = {
            'birthdate': DateInput()
        }