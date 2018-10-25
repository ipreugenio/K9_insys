from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='deployment'
urlpatterns = [
    path('', views.index, name='index'),
    path('dogs-deployed', views.deployed_dogs, name='deployed_dogs'),
    path('dogs-requested', views.requested_dogs, name='requested_dogs'),
    path('deploy-number-dogs', views.deploy_number_dogs, name='deploy_number_dogs'),
    path('location-form', views.location_form, name='location_form'),
    path('assign_team/', views.assign_team, name='assign_team'),
    path('load-teams/', views.load_teams, name='ajax_load_teams'),  # <-- this one here
    path('area_list/', views.area_list_view, name='area_list'),
    path('area_detail/<int:id>', views.area_detailview, name='area_detail'),
    #path('/<int:id>/', views., name=''),
];