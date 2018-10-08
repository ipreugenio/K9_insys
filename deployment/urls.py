from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='deployment'
urlpatterns = [
    path('', views.index, name='index'),
    path('dogs-deployed', views.deployed_dogs, name='deployed_dogs'),
    path('dogs-requested', views.requested_dogs, name='requested_dogs'),
    path('deploy-number-dogs', views.deploy_number_dogs, name='deploy_number_dogs'),
    #path('/<int:id>/', views., name=''),
];