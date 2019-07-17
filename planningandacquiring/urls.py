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
    path('add_K9_offspring/<int:id>', views.add_K9_offspring, name='add_K9_offspring'),
    path('no_litter/<int:id>', views.no_litter, name='no_litter'),
    path('add_K9_parents_form/confirm_K9_parents/add_K9_offspring_form/confirm_breeding/', views.confirm_breeding, name='confirm_breeding'),
    path('breeding_confirmed/', views.breeding_confirmed, name='breeding_confirmed'),
    path('K9_list/', views.K9_listview, name='K9_list'),
    path('K9_detail/<int:id>', views.K9_detailview, name='K9_detail'),
    path('report/', views.report, name='report'),
    path('index/', views.index, name='index'),
    path('K9_forecast/', views.forecast_result, name='K9_forecast'),
    path('breeding_recommendation/', views.breeding_recommendation, name = 'breeding_recommendation'),

    path('budgeting/', views.budgeting, name = 'budgeting'),
    path('budget_list/budgeting/', views.budgeting, name = 'budgeting'),
    path('budget_list/', views.budgeting_list, name='budget_list'),

    path('budget_report/', views.budgeting_report, name='budget_report'),

    path('add_breed_form/', views.add_breed, name='add_breed_form'),
    path('view_breed/', views.breed_listview, name='view_breed'),
    path('breed_list/', views.breed_list, name='breed_list'),
    path('breed_detail/<int:id>', views.breed_detail, name='breed_detail'),
    path('mating_confirmed/', views.mating_confirmed, name='mating_confirmed'),

    path('breeding_list/', views.breeding_list, name='breeding_list'),
    path('breeding_k9_confirmed/', views.breeding_k9_confirmed, name='breeding_k9_confirmed'),
    
    path('add_supplier/', views.add_supplier, name='add_supplier'),
    path('add_procured_k9/', views.add_procured_k9, name='add_procured_k9'),
    
    path('add_procured_k9/ajax_load_supplier', views.load_supplier, name='ajax_load_supplier'),
    path('add_K9_parents_form/ajax_load_k9_reco', views.load_k9_reco, name='ajax_load_k9_reco'),

    path('accomplishment_date/', views.accomplishment_date, name='accomplishment_date'),
    path('accomplishment_date/accomplishment_report/', views.accomplishment_report, name='accomplishment_report'),

    path('vet_date/', views.vet_date, name='vet_date'),
    path('vet_date/vet_report/', views.vet_report, name='vet_report'),

    path('inventory_date/', views.inventory_date, name='inventory_date'),
    path('inventory_date/inventory_report/', views.inventory_report, name='inventory_report'),
];

