from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='inventory'
urlpatterns = [
    path('', views.index, name='index'),
    #Medicine
    path('add-medicine', views.medicine_add, name='medicine_add'),
    path('list-medicine', views.medicine_list, name='medicine_list'),
    path('edit-medicine/<int:id>/', views.medicine_edit, name='medicine_edit'),
    path('delete-medicine/<int:id>/', views.medicine_delete, name='medicine_delete'),
    #Food
    path('add-food', views.food_add, name='food_add'),
    path('list-food', views.food_list, name='food_list'),
    path('edit-food/<int:id>/', views.food_edit, name='food_edit'),
    path('delete-food/<int:id>/', views.food_delete, name='food_delete'),
    #Miscellaneous
    path('add-miscellaneous', views.miscellaneous_add, name='miscellaneous_add'),
    path('list-miscellaneous', views.miscellaneous_list, name='miscellaneous_list'),
    path('edit-miscellaneous/<int:id>/', views.miscellaneous_edit, name='miscellaneous_edit'),
    path('delete-miscellaneous/<int:id>/', views.miscellaneous_delete, name='miscellaneous_delete'),
    #Inventory
    path('list-medicine-inventory', views.medicine_inventory_list, name='medicine_inventory_list'),
    path('list-food-inventory', views.food_inventory_list, name='food_inventory_list'),
    path('list-miscellaneous-inventory', views.miscellaneous_inventory_list, name='miscellaneous_inventory_list'),
    #inventory Count List
    path('medicine-inventory-count/<int:id>/', views.medicine_inventory_count, name='medicine_inventory_count'),
    path('food-inventory-count/<int:id>/', views.food_inventory_count, name='food_inventory_count'),
    path('miscellaneous-inventory-count/<int:id>/', views.miscellaneous_inventory_count, name='miscellaneous_inventory_count'),
    #inventory Count Form
    path('medicine-count-form/<int:id>/', views.medicine_count_form, name='medicine_count_form'),
    path('food-count-form/<int:id>/', views.food_count_form, name='food_count_form'),
    path('miscellaneous-count-form/<int:id>/', views.miscellaneous_count_form, name='miscellaneous_count_form'),
    #inventory Receive Form
    path('medicine-receive-form/<int:id>/', views.medicine_receive_form, name='medicine_receive_form'),
    path('food-receive-form/<int:id>/', views.food_receive_form, name='food_receive_form'),
    path('miscellaneous-receive-form/<int:id>/', views.miscellaneous_receive_form, name='miscellaneous_receive_form'),
];