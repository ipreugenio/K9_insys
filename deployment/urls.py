from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='deployment'
urlpatterns = [
    path('', views.index, name='index'),
    path('add-area/', views.add_area, name='add_area'),
    path('add-location/', views.add_location, name='add_location'),
    path('assign-team-location/', views.assign_team_location, name='assign_team_location'),
    path('assigned-location-list/', views.assigned_location_list, name='assigned_location_list'),
    path('team-location-details/<int:id>', views.team_location_details, name='team_location_details'),
    path('edit-team/<int:id>', views.edit_team, name='edit_team'),
];
