from django.contrib import admin
from unitmanagement.models import Health, HealthMedicine, PhysicalExam, VaccinceRecord, VaccineUsed
from unitmanagement.models import K9_Incident, Handler_Incident

# Register your models here.
admin.site.register(Health)
admin.site.register(HealthMedicine)
admin.site.register(PhysicalExam)
admin.site.register(VaccinceRecord)
admin.site.register(VaccineUsed)
admin.site.register(K9_Incident)
admin.site.register(Handler_Incident)
