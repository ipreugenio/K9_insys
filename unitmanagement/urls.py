from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='unitmanagement'
urlpatterns = [
    path('', views.index, name='index'),
    path('health-form', views.health_form, name='health_form'),
    path('physical-exam-form', views.physical_exam_form, name='physical_exam_form'),
    path('health-record', views.health_record, name='health_record'),
    path('health-history/<int:id>', views.health_history, name='health_history'),
    path('health-details/<int:id>', views.health_details, name='health_details'),
    path('physical-exam-details/<int:id>', views.physical_exam_details, name='physical_exam_details'),
    path('approve-medicine/<int:id>', views.medicine_approve, name='medicine_approve'),
    path('vaccination-form', views.vaccination_form, name='vaccination_form'),
    path('vaccination', views.vaccination, name='vaccination'),
    path('request-form', views.requests_form, name='request_form'),
    path('request-list', views.request_list, name='request_list'),
    path('change-equipment/<int:id>', views.change_equipment, name='change_equipment'),
    #path('/<int:id>/', views., name=''),
];