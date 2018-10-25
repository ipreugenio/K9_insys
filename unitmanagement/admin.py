from django.contrib import admin
from unitmanagement.models import Health, HealthMedicine, PhysicalExam, VaccinceRecord

# Register your models here.
admin.site.register(Health)
admin.site.register(HealthMedicine)
admin.site.register(PhysicalExam)
admin.site.register(VaccinceRecord)