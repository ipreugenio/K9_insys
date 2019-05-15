from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from planningandacquiring.models import K9
from training.models import K9_Handler, Training, K9_Adopted_Owner, Record_Training
from profiles.models import User
from unitmanagement.models import Handler_K9_History

class DateInput(forms.DateInput):
    input_type = 'date'


class ClassifySkillForm(forms.Form):
    CHOICES = (
        ('SAR', 'SAR'),
        ('NDD', 'NDD'),
        ('EDD', 'EDD'),
    )

    skill = forms.ChoiceField(choices=CHOICES,
                               widget=forms.RadioSelect)


class TestForm(forms.Form):
    k9 = forms.ModelChoiceField(queryset=K9.objects.all())

class add_handler_form(forms.ModelForm):
    handler = forms.ModelChoiceField(queryset = User.objects.filter(status='Working').filter(position='Handler').filter(partnered=False))
    
    class Meta:
        model = K9_Handler
        fields = ('handler',)

    # def __init__(self, *args, **kwargs):
    #     super(add_handler_form, self).__init__(*args, **kwargs)
    #     self.fields['handler'].queryset = self.fields['handler'].queryset.exclude(position="Veterinarian")
    #     self.fields['handler'].queryset = self.fields['handler'].queryset.exclude(position="Administrator")
    #     assigned_handler = K9_Handler.objects.all()
    #     assigned_handler_list = []
    #     for handler in assigned_handler:
    #         assigned_handler_list.append(handler.id)
    #     self.fields['handler'].queryset = self.fields['handler'].queryset.exclude(pk__in=assigned_handler_list)

class assign_handler_form(forms.ModelForm): 
    handler = forms.ModelChoiceField(queryset = User.objects.filter(status='Working').filter(position='Handler').filter(partnered=False),
    widget=forms.RadioSelect(), empty_label=None)
    
    class Meta:
        model = Handler_K9_History
        fields = ('handler','k9')

    def __init__(self, *args, **kwargs):
        super(assign_handler_form, self).__init__(*args, **kwargs)
        self.fields['handler'].required = False
        self.fields['k9'].required = False


class TrainingUpdateForm(forms.ModelForm):
    GRADE = (
        ('75.0', '75.0'),
        ('80.0', '80.0'),
        ('85.0', '85.0'),
        ('90.0', '90.0'),
        ('95.0', '95.0'),
        ('100.0', '100.0'),
    )
    remarks = forms.CharField(widget = forms.Textarea(attrs={'rows':'3', 'style':'resize:none;'}))
    grade = forms.CharField(widget = forms.Select(choices=GRADE))

    class Meta:
        model = Training
        fields = ('stage1_1', 'stage1_2', 'stage1_3', 'stage2_1', 'stage2_2', 'stage2_3', 'stage3_1',
        'stage3_2', 'stage3_3', 'grade', 'remarks')

    def __init__(self, *args, **kwargs):
        super(TrainingUpdateForm, self).__init__(*args, **kwargs)
        self.fields['grade'].required = False
        self.fields['remarks'].required = False

class SerialNumberForm(forms.Form):
    DOG_TYPE=(
        ('For-Deployment', 'For-Deployment'),
        ('For-Breeding', 'For-Breeding'),
    )
    #microchip = forms.CharField(max_length=200)
    dog_type = forms.CharField(max_length=200, widget = forms.Select(choices=DOG_TYPE))

class AdoptionForms(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':'2', 'style':'resize:none;'}))

    class Meta:
        model = K9_Adopted_Owner
        fields = ('first_name', 'middle_name', 'last_name', 'sex', 'birth_date','email', 'contact_no', 'address')
        widgets = {
            'birth_date': DateInput(),
        }

class RecordForm(forms.ModelForm):

    class Meta:
        model = Record_Training
        fields = ('on_leash', 'off_leash', 'obstacle_course', 'panelling', 'port_plant', 'port_find', 'port_time', 'building_plant', 'building_find',
                  'building_time', 'vehicle_plant', 'vehicle_find', 'vehicle_time', 'baggage_plant', 'baggage_find', 'baggage_time',
                  'others_plant', 'others_find', 'others_time', 'daily_rating', 'MARSEC', 'MARLEN', 'MARSAR', 'MAREP', 'morning_feed', 'evening_feed')


class DateForm(forms.Form):
    choose_date = forms.DateField( widget=DateInput())
    # input_type = 'date'
    #input_type = 'date'
    # format='%Y/%m/%d'),
    #                                   input_formats=('%Y/%m/%d',

