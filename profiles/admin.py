from django.contrib import admin

from profiles.models import User, Personal_Info
# Register your models here.

admin.site.register(User)
admin.site.register(Personal_Info)
