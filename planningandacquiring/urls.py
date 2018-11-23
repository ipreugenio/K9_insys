from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='planningandacquiring'
urlpatterns = [
    path('', views.index, name='index'),
    #path('/<int:id>/', views., name=''),
    path('add_donated_K9_form/', views.add_donated_K9, name='add_donated_K9_form'),
    #path('add_donated_K9_form/add_donator_form/', views.add_donator, name='add_donator_form'),
    path('add_donated_K9_form/confirm_donation/', views.confirm_donation, name='confirm_donation'),
    path('donation_confirmed/', views.donation_confirmed, name='donation_confirmed'),
    path('add_K9_parents_form/', views.add_K9_parents, name='add_K9_parents_form'),
    path('add_K9_parents_form/confirm_K9_parents/', views.confirm_K9_parents, name='confirm_K9_parents'),
    path('add_K9_parents_form/confirm_K9_parents/K9_parents_confirmed', views.K9_parents_confirmed, name='K9_parents_confirmed'),
    path('add_K9_parents_form/confirm_K9_parents/add_K9_offspring_form/', views.add_offspring_K9, name='add_K9_offspring_form'),
    path('add_K9_parents_form/confirm_K9_parents/add_K9_offspring_form/confirm_breeding/', views.confirm_breeding, name='confirm_breeding'),
    path('breeding_confirmed/', views.breeding_confirmed, name='breeding_confirmed'),
    path('K9_list/', views.K9_listview, name='K9_list'),
    path('K9_detail/<int:id>', views.K9_detailview, name='K9_detail'),
    path('report/', views.report, name='report'),
    path('index/', views.index, name='index'),
    path('K9_forecast/', views.forecast_result, name='K9_forecast'),
    path('breeding_recommendation/', views.breeding_recommendation, name = 'breeding_recommendation'),
    path('budgeting/', views.budgeting, name = 'budgeting')
];

