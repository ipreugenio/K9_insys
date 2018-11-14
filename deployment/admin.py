from django.contrib import admin

from deployment.models import Area, Location, Team_Assignment, Team_Dog_Deployed
# Register your models here.
admin.site.register(Area)
admin.site.register(Location)
admin.site.register(Team_Assignment)
admin.site.register(Team_Dog_Deployed)
