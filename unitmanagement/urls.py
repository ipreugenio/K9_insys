from django.urls import path
from django.conf.urls import include, url
from .import views
from django.views.generic import TemplateView

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
    path('request-form', views.requests_form, name='request_form'),
    path('request-list', views.request_list, name='request_list'),
    path('change-equipment/<int:id>', views.change_equipment, name='change_equipment'),
    path('k9-incident', views.k9_incident, name='k9_incident'),
    path('handler-incident', views.handler_incident, name='handler_incident'),
    path('reassign-assets', views.reassign_assets, name='reassign_assets'),
    path('choose-date/', views.choose_date, name='choose_date'),
    path('choose-date/um-report/', views.um_report, name='um_report'),
    path('reproductive-list', views.reproductive_list, name='reproductive_list'),
    path('reproductive-edit/<int:id>', views.reproductive_edit, name='reproductive_edit'),
    path('k9-unpartnered-list', views.k9_unpartnered_list, name='k9_unpartnered_list'),
    path('choose-handler-list/<int:id>', views.choose_handler_list, name='choose_handler_list'),
    path('choose-handler/<int:id>', views.choose_handler, name='choose_handler'),
    path('k9-sick-list', views.k9_sick_list, name='k9_sick_list'),
    path('k9-sick-details/<int:id>', views.k9_sick_details, name='k9_sick_details'),
    path('on-leave-request', views.on_leave_request, name='on_leave_request'),
    path('on-leave-list', views.on_leave_list, name='on_leave_list'),
    path('on-leave-details/<int:id>', views.on_leave_details, name='on_leave_details'),

    path('redirect-notif/<int:id>', views.redirect_notif, name='redirect_notif'),
    # path('ajax/load-handler/', views.load_hander, name='ajax_load_handler'),

    path('k9/api', views.K9ListView.as_view()),
    path('user/api', views.UserListView.as_view()),
    path('k9/api/<int:id>', views.K9DetailView.as_view()),
    path('user/api/<int:id>', views.UserDetailView.as_view()),

    #path('/<int:id>/', views., name=''),
];