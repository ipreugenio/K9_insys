from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from .models import User, Personal_Info


class DateInput(forms.DateInput):
    input_type = 'date'

class add_User_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ('serial_number', 'firstname', 'lastname', 'nickname', 'position', 'rank', 'extensionname', 'middlename',
                  'gender', 'birthdate', 'birthplace', 'civilstatus', 'citizenship', 'religion', 'bloodtype',
                  'distinct_feature', 'haircolor', 'eyecolor', 'skincolor', 'height', 'weight',
                  'headsize', 'footsize', 'bodybuild')
        widgets = {
            'birthdate': DateInput()
        }

class add_personal_form(forms.ModelForm):
    class Meta:
        model = Personal_Info
        fields = ('mobile_number', 'email_address', 'tel_number', 'street',
                  'barangay', 'city', 'province', 'mother_name', 'mother_birthdate',
                  'father_name', 'father_birthdate', 'tin', 'philhealth')
        widgets = {
            'father_birthdate': DateInput(),
            'mother_birthdate': DateInput()
        }