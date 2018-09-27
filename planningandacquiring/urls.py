from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='planningandacquiring'
urlpatterns = [
    path('', views.index, name='index'),
    #path('/<int:id>/', views., name=''),
    path('add_K9_form/', views.add_K9, name='add_K9_form'),
];