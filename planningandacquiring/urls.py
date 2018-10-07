from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='planningandacquiring'
urlpatterns = [
    path('', views.index, name='index'),
    #path('/<int:id>/', views., name=''),
    path('add_K9_form/', views.add_donated_K9, name='add_K9_form'),
    path('add_K9_form/add_donator_form/', views.add_donator, name='add_donator_form'),
    path('add_K9_form/add_donator_form/confirm_donation/', views.confirm_donation, name='confirm_donation'),
    path('donation_confirmed/', views.donation_confirmed, name='donation_confirmed'),
    path('K9_list/', views.K9_listview, name='K9_list'),
    path('K9_detail/<int:id>', views.K9_detailview, name='K9_detail'),
];