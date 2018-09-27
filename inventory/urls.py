from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='inventory'
urlpatterns = [
    path('', views.index, name='index'),
    #Medicine
    path('add-medicine', views.medicine_add, name='medicine_add'),
    path('list-medicine', views.medicine_list, name='medicine_list'),
    path('delete-medicine/<int:id>/', views.medicine_delete, name='medicine_delete'),
    #Food
    path('add-food', views.food_add, name='food_add'),
    path('list-food', views.food_list, name='food_list'),
    path('delete-food/<int:id>/', views.food_delete, name='food_delete'),
    #Equipment
    path('add-equipment', views.equipment_add, name='equipment_add'),
    path('list-equipment', views.equipment_list, name='equipment_list'),
    path('delete-equipment/<int:id>/', views.equipment_delete, name='equipment_delete'),

    #path('/<int:id>/', views., name=''),
];