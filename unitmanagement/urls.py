from django.urls import path
from django.conf.urls import include, url
from .import views
from django.views.generic import TemplateView

app_name='unitmanagement'
urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('health-form', views.health_form, name='health_form'),
    path('physical-exam-form', views.physical_exam_form, name='physical_exam_form'),
    path('health-record', views.health_record, name='health_record'),
    path('health-history/<int:id>', views.health_history, name='health_history'),
    path('health-history-handler', views.health_history_handler, name='health_history_handler'),
    path('health-details/<int:id>', views.health_details, name='health_details'),
    path('physical-exam-details/<int:id>', views.physical_exam_details, name='physical_exam_details'),
    path('approve-medicine/<int:id>', views.medicine_approve, name='medicine_approve'),
    path('request-form', views.requests_form, name='request_form'),
    #path('request-list', views.request_list, name='request_list'),
    path('k9-incident', views.k9_incident, name='k9_incident'),
    path('handler-incident-form', views.handler_incident_form, name='handler_incident_form'),
    path('reproductive-list', views.reproductive_list, name='reproductive_list'),
    path('reproductive-edit/<int:id>', views.reproductive_edit, name='reproductive_edit'),
    path('k9-unpartnered-list', views.k9_unpartnered_list, name='k9_unpartnered_list'),
    path('choose-handler-list/<int:id>', views.choose_handler_list, name='choose_handler_list'),
    path('choose-handler/<int:id>', views.choose_handler, name='choose_handler'),
    path('k9-sick-form', views.k9_sick_form, name='k9_sick_form'),
    path('k9-sick-list', views.k9_sick_list, name='k9_sick_list'),
    path('k9-sick-details/<int:id>', views.k9_sick_details, name='k9_sick_details'),
    path('on-leave-request', views.on_leave_request, name='on_leave_request'),
    path('on-leave-list', views.on_leave_list, name='on_leave_list'),
    path('on-leave-decision/<int:id>', views.on_leave_decision, name='on_leave_decision'),

    path('health-list', views.health_list_handler, name='health_list_handler'),
    path('k9-incident-list', views.k9_incident_list, name='k9_incident_list'),
    path('k9-retrieved/<int:id>', views.k9_retreived, name='k9_retreived'),
    path('follow-up/<int:id>', views.follow_up, name='follow_up'),

    #path('choose-date/<int:id>', views.choose_date, name='choose_date'),

    path('redirect-notif/<int:id>', views.redirect_notif, name='redirect_notif'),
    # path('ajax/load-handler/', views.load_hander, name='ajax_load_handler'),

    path('choose-handler-list/ajax_load_handler', views.load_handler, name='ajax_load_handler'),
    path('health-history/ajax_load_stamp', views.load_stamp, name='ajax_load_stamp'),
    path('ajax_load_k9', views.load_k9, name='ajax_load_k9'),
    path('k9-sick-details/ajax_load_health', views.load_health, name='ajax_load_health'),
    path('k9-incident-list/ajax_load_incident', views.load_incident, name='ajax_load_incident'),

    
    path('vaccination_form', views.vaccination_form, name='vaccination_form'),
    path('reassign-assets', views.reassign_assets, name='reassign_assets'),
    #path('change-equipment/<int:id>', views.change_equipment, name='change_equipment'),
    path('confirm-death/<int:id>', views.confirm_death, name='confirm_death'),
    
    path('team-leader/api', views.TeamLeaderView.as_view()),
    path('handler/api', views.HandlerView.as_view()),
    path('vet/api', views.VetView.as_view()),


    path('k9-checkup-pending', views.k9_checkup_pending, name='k9_checkup_pending'),
    path('ajax_load_appointments', views.load_appointments, name='ajax_load_appointments'),
    path('ajax_load_checkups', views.load_checkups, name='ajax_load_checkups')



    #path('/<int:id>/', views., name=''),
];