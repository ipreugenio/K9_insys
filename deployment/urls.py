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
    path('remove-dog-deployed/<int:id>', views.remove_dog_deployed, name='remove_dog_deployed'),
    path('request_form/', views.dog_request, name='request_form'),
    path('request_dog_list/', views.request_dog_list, name='request_dog_list'),
    path('request_dog_list/$', views.request_dog_list, name='request_dog_list'), #DON"T DELETE
    path('request_dog_list/deployment/request_dog_details/<int:id>', views.request_dog_details, name='request_dog_details'),
    path('request_dog_details/<int:id>', views.request_dog_details, name='request_dog_details'),
    path('remove-dog-request/<int:id>', views.remove_dog_request, name='remove_dog_request'),
    path('view-schedule/<int:id>', views.view_schedule, name='view_schedule'),
    path('view-schedule/deployment/request_dog_details/<int:id>', views.request_dog_details, name='request_dog_details'),
    path('view-schedule/deployment/request_dog_list/deployment/request_dog_details/<int:id>', views.request_dog_details, name='request_dog_details'),
    path('view-schedule/deployment/request_dog_list/', views.request_dog_list, name='request_dog_list'),
    path('add-incident/', views.add_incident, name='add_incident'),
    path('view-incidents/', views.incident_list, name='view_incidents'),

    path('incident-detail/<int:id>', views.incident_detail, name='incident_detail'),

    path('choose-date/', views.choose_date, name='choose_date'),
    path('choose-date/deployment-report/', views.deployment_report, name='deployment_report'),


    # path('dogs-deployed', views.deployed_dogs, name='deployed_dogs'),
    # path('dogs-requested', views.requested_dogs, name='requested_dogs'),
    # path('deploy-number-dogs', views.deploy_number_dogs, name='deploy_number_dogs'),
    # path('location-form', views.location_form, name='location_form'),
    # path('assign_team/', views.assign_team, name='assign_team'),
    # path('load-teams/', views.load_teams, name='ajax_load_teams'),  # <-- this one here
    # path('area_list/', views.area_list_view, name='area_list'),
    # path('add_location/', views.area_form, name='add_location'),
    # path('add_team/', views.team_form, name='add_team'),
    # path('area_detail/<int:id>', views.area_list_detail, name='area_detail'),
    #path('/<int:id>/', views., name=''),
];
