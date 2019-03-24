from django import forms
from django.forms import ModelForm, ValidationError, Form, widgets
from django.contrib.admin.widgets import AdminDateWidget
from datetime import date, datetime
from django.forms import formset_factory, inlineformset_factory
from django.contrib.sessions.models import Session

from unitmanagement.models import PhysicalExam , Health, HealthMedicine, VaccinceRecord, Requests, VaccineUsed
from unitmanagement.models import K9_Incident, Handler_Incident
from planningandacquiring.models import K9
from inventory.models import Medicine, Miscellaneous, Medicine_Inventory
from profiles.models import Account, User

def user_in_session(request):
    serial = request.session['session_serial']
    account = Account.objects.get(serial_number=serial)
    user_in_session = User.objects.get(id=account.UserID.id)   
    return user_in_session.id

class DateInput(forms.DateInput):
    input_type = 'date'

class PhysicalExamForm(forms.ModelForm):
    EXAMSTATUS = (
        ('Normal', 'Normal'),
        ('Abnormal', 'Abnormal'),
        ('Not Examined', 'Not Examined'),
    )
    #dog = forms.ModelChoiceField(queryset = K9.objects.all().order_by('name'))
    general_appearance = forms.CharField(label = 'general_appearance', widget = forms.Select(choices=EXAMSTATUS))
    integumentary = forms.CharField(label = 'integumentary', widget = forms.Select(choices=EXAMSTATUS))
    musculo_skeletal = forms.CharField(label = 'musculo_skeletal', widget = forms.Select(choices=EXAMSTATUS))
    respiratory = forms.CharField(label = 'respiratory', widget = forms.Select(choices=EXAMSTATUS))
    genito_urinary = forms.CharField(label = 'genito_urinary', widget = forms.Select(choices=EXAMSTATUS))
    nervous = forms.CharField(label = 'nervous', widget = forms.Select(choices=EXAMSTATUS))
    circulatory = forms.CharField(label = 'circulatory', widget = forms.Select(choices=EXAMSTATUS))
    digestive = forms.CharField(label = 'digestive', widget = forms.Select(choices=EXAMSTATUS))
    mucous_membrances = forms.CharField(label = 'mucous_membrances', widget = forms.Select(choices=EXAMSTATUS))
    lymph_nodes = forms.CharField(label = 'lymph_nodes', widget = forms.Select(choices=EXAMSTATUS))
    eyes = forms.CharField(label = 'eyes', widget = forms.Select(choices=EXAMSTATUS))
    ears = forms.CharField(label = 'ears', widget = forms.Select(choices=EXAMSTATUS))
    remarks = forms.CharField(label = 'remarks', widget = forms.Textarea(attrs={'rows':'4'}))

    class Meta:
        model = PhysicalExam
        fields = ('dog', 'cage_number', 'general_appearance', 'integumentary',
        'musculo_skeletal', 'respiratory', 'genito_urinary', 'nervous', 'circulatory', 'digestive',
        'mucous_membrances', 'lymph_nodes', 'eyes', 'ears', 'remarks', 'date_next_exam')

    def __init__(self, *args, **kwargs):
        super(PhysicalExamForm, self).__init__(*args, **kwargs)
        self.fields['cage_number'].required = False
        self.fields['remarks'].required = False
        self.fields['date_next_exam'].required = False
        # a = K9.objects.filter(id=request.session['phex_k9_id'])
        # self.fields['dog'].initial = a

class HealthForm(forms.ModelForm):
    treatment = forms.CharField(widget = forms.Textarea(attrs={'rows':'4'}))
    
    class Meta:
        model = Health
        fields = ('dog','problem', 'treatment', 'incident_id')

    def __init__(self, *args, **kwargs):
        super(HealthForm, self).__init__(*args, **kwargs)
        self.fields['dog'].required = False
        self.fields['problem'].required = False
        self.fields['incident_id'].required = False

class HealthMedicineForm(forms.ModelForm):
    TIME_OF_DAY = (
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Night', 'Night'),
        ('Morning/Afternoon', 'Morning/Afternoon'),
        ('Morning/Night', 'Morning/Night'),
        ('Afternoon/Night', 'Afternoon/Night'),
        ('Morning/Afternoon/Night', 'Morning/Afternoon/Night'),
    )

    class Meta:
        model = HealthMedicine
        fields = ('medicine', 'quantity', 'time_of_day', 'duration')

    medicine = forms.ModelChoiceField(queryset = Medicine_Inventory.objects.exclude(quantity=0).exclude(medicine__med_type='Vaccine').exclude(medicine__med_type='Vitamins'))
    time_of_day = forms.CharField(label = 'Time of Day', widget = forms.Select(choices=TIME_OF_DAY))
    duration = forms.IntegerField(label = 'Duration (Days)')

    def __init__(self, *args, **kwargs):
        super(HealthMedicineForm, self).__init__(*args, **kwargs)
        self.fields['medicine'].required = False

class VaccinationRecordForm(forms.ModelForm):

    class Meta:
        model = VaccinceRecord
        fields = ('deworming_1', 'deworming_2', 'deworming_3', 'dhppil_cv_1', 'heartworm_1', 'bordetella_1', 
        'tick_flea_1', 'dhppil_cv_2', 'deworming_4', 'heartworm_2', 'bordetella_2', 'anti_rabies', 'tick_flea_2',
        'dhppil_cv_3', 'heartworm_3', 'dhppil4_1', 'tick_flea_3', 'dhppil4_2', 'heartworm_4', 'tick_flea_4', 
        'heartworm_5', 'tick_flea_5', 'heartworm_6', 'tick_flea_6', 'heartworm_7', 'tick_flea_7', 'heartworm_8')

    def __init__(self, *args, **kwargs):
        super(VaccinationRecordForm, self).__init__(*args, **kwargs)
        self.fields['deworming_1'].required = False
        self.fields['deworming_2'].required = False
        self.fields['deworming_3'].required = False
        self.fields['dhppil_cv_1'].required = False
        self.fields['heartworm_1'].required = False
        self.fields['bordetella_1'].required = False
        self.fields['tick_flea_1'].required = False
        self.fields['dhppil_cv_2'].required = False
        self.fields['deworming_4'].required = False
        self.fields['heartworm_2'].required = False
        self.fields['bordetella_2'].required = False
        self.fields['anti_rabies'].required = False
        self.fields['tick_flea_2'].required = False
        self.fields['dhppil_cv_3'].required = False
        self.fields['heartworm_3'].required = False
        self.fields['tick_flea_3'].required = False
        self.fields['dhppil4_2'].required = False
        self.fields['heartworm_4'].required = False
        self.fields['tick_flea_4'].required = False
        self.fields['heartworm_5'].required = False
        self.fields['tick_flea_5'].required = False
        self.fields['heartworm_6'].required = False
        self.fields['tick_flea_6'].required = False
        self.fields['heartworm_7'].required = False
        self.fields['tick_flea_7'].required = False
        self.fields['heartworm_8'].required = False

class VaccinationUsedForm(forms.Form):
    vaccine = forms.ModelChoiceField(queryset = Medicine.objects.filter(med_type = "Vaccine").filter(med_type = "Others").order_by('medicine'))


class RequestForm(forms.ModelForm):
    CONCERN = (
        ('Broken', 'Broken'),
        ('Lost', 'Lost'),
        ('Stolen', 'Stolen'),
    )
    handler = forms.ModelChoiceField(queryset = User.objects.all())
    concern = forms.CharField(max_length=10, label='concern', widget=forms.Select(choices=CONCERN))
    equipment = forms.ModelChoiceField(queryset=Miscellaneous.objects.filter(misc_type="Equipment").order_by('miscellaneous'))
    remarks = forms.CharField(widget = forms.Textarea(attrs={'rows':'3', 'style':'resize:none;'}))

    class Meta:
        model = Requests
        fields = ('handler', 'equipment', 'remarks', 'concern')

    def __init__(self, *args, **kwargs):
        super(RequestForm, self).__init__(*args, **kwargs)
        self.fields['handler'].required = False
        
class K9IncidentForm(forms.ModelForm):
    
    k9 = forms.ModelChoiceField(queryset = K9.objects.all())

    class Meta:
        model = K9_Incident
        fields = ('k9', 'incident', 'description', 'reported_by')

    def __init__(self, *args, **kwargs):
        super(K9IncidentForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['reported_by'].required = False

class HandlerIncidentForm(forms.ModelForm):
    INCIDENT = (
        #('Accident', 'Accident'),
        ('Died', 'Died'),
    )
    
    handler = forms.ModelChoiceField(queryset = User.objects.filter(position='Handler').exclude(status='Retired').exclude(status='Dead'))
    incident = forms.CharField(widget = forms.Select(choices=INCIDENT))
    
    class Meta:
        model = Handler_Incident
        fields = ('handler', 'incident', 'description')

    def __init__(self, *args, **kwargs):
        super(HandlerIncidentForm, self).__init__(*args, **kwargs)
        self.fields['description'].required = False

class HandlerOnLeaveForm(forms.ModelForm):
    incident = forms.CharField()
    handler = forms.ModelChoiceField(queryset = User.objects.filter(position='Handler').exclude(status='Retired').exclude(status='Dead'))
    class Meta:
        model = Handler_Incident
        fields = ('handler', 'incident', 'description', 'date_from', 'date_to')

        widgets = {
            'date_from': DateInput(),
            'date_to': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(HandlerOnLeaveForm, self).__init__(*args, **kwargs)
        self.fields['incident'].initial = 'On-Leave'
       

class ReassignAssetsForm(forms.Form):
    k9 = forms.ModelChoiceField(queryset = K9.objects.filter(training_status='For-Deployment').filter(partnered=False))
    handler = forms.ModelChoiceField(queryset = User.objects.filter(status='Working').filter(position='Handler').filter(partnered=False))

class DateForm(forms.Form):
    from_date = forms.DateField( widget=DateInput())
    to_date = forms.DateField(widget=DateInput())
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['handler'].queryset = User.objects.none()
    #     if 'k9' in self.data:
    #         try:
    #             k9_capability = str(self.data.get('k9').capability)
    #             self.fields['handler'].queryset = User.objects.filter(handler_id=k9_capability).filter(status='Working').filter(position='Handler').filter(partnered=False)
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #          self.fields['handler'].queryset = self.k9.handler.order_by('name')

class ReproductiveForm(forms.ModelForm):
    class Meta:
        model = K9
        fields = ('reproductive_stage', 'last_proestrus_date', 'in_heat_months')

        widgets = {
            'last_proestrus_date': DateInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super(ReproductiveForm, self).__init__(*args, **kwargs)
        self.fields['last_proestrus_date'].required = False

