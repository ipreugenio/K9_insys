from django.contrib import admin
from .models import Training, K9_Handler,Training_History,Training_Schedule
# Register your models here.

admin.site.register(Training)
admin.site.register(K9_Handler)
admin.site.register(Training_History)
admin.site.register(Training_Schedule)
