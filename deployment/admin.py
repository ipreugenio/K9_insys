from django.contrib import admin

from deployment.models import Location, Area, Team
# Register your models here.
admin.site.register(Location)
admin.site.register(Area)
admin.site.register(Team)