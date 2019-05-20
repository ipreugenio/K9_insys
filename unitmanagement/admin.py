from django.contrib import admin
from unitmanagement.models import Health, HealthMedicine, PhysicalExam, VaccinceRecord, VaccineUsed, Transaction_Health
from unitmanagement.models import K9_Incident, Handler_Incident, Notification, Equipment_Request, Handler_K9_History, Image, Handler_On_Leave

# Register your models here.
admin.site.register(Health)
admin.site.register(HealthMedicine)
admin.site.register(PhysicalExam)
admin.site.register(VaccinceRecord)
admin.site.register(VaccineUsed)
admin.site.register(K9_Incident)
admin.site.register(Handler_Incident)
admin.site.register(Handler_On_Leave)
admin.site.register(Notification)
admin.site.register(Equipment_Request)
admin.site.register(Handler_K9_History)
admin.site.register(Image)
admin.site.register(Transaction_Health)
