from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='training'
urlpatterns = [
    path('', views.index, name='index'),

    path('list-classify-k9', views.classify_k9_list, name='classify_k9_list'),
    path('classify-k9/<int:id>', views.classify_k9_select, name='classify_k9_select'),
    path('training-record', views.training_records, name='training_records'),
    path('assign-k9/<int:id>', views.assign_k9_select, name='assign_k9_select'),
    path('training-update/<int:id>', views.training_update_form, name='training_update_form'),
    path('training-finalization/<int:id>', views.serial_number_form, name='serial_number_form'),

    path('training-details/<int:id>', views.training_details, name='training_details'),

    path('choose-date/<int:id>', views.choose_date, name='choose_date'),
    path('choose-date/daily-record/', views.daily_record, name='daily_record'),  # the record itself
    path('record-daily/', views.record_form, name='record_daily'), #form for recording of refresher

    path('k9-record', views.k9_record, name='k9_record'), #list ng k9 with records

    path('fail-dog/<int:id>', views.fail_dog, name='fail_dog'),
    path('view_graph/<int:id>', views.view_graphs, name='view_graph'),

    path('training/list-classify-k9', views.classify_k9_list, name='classify_k9_list'),
    path('training/classify-k9/<int:id>', views.classify_k9_select, name='classify_k9_select'),
    path('training/training-records', views.training_records, name='training_records'),

    path('training/genealogy/<int:id>', views.view_family_tree, name='genealogy'),
    path('training/assign-k9/<int:id>', views.assign_k9_select, name='assign_k9_select'),
    path('training/training-update/<int:id>', views.training_update_form, name='training_update_form'),
    path('training/training-finalization/<int:id>', views.serial_number_form, name='serial_number_form'),
    path('training/training-details/<int:id>', views.training_details, name='training_details'),
    path('training/fail-dog/<int:id>', views.fail_dog, name='fail_dog'),
    path('addoption/adoption-list', views.adoption_list, name='adoption_list'),
    path('addoption/adoption-form/<int:id>', views.adoption_form, name='adoption_form'),
    path('addoption/confirm-adoption/<int:id>', views.confirm_adoption, name='confirm_adoption'),
    path('addoption/adoption-confirmed', views.adoption_confirmed, name='adoption_confirmed'),
    path('addoption/adoption-details/<int:id>', views.adoption_details, name='adoption_details'),

    path('list-training-k9', views.k9_training_list, name='k9_training_list'),

    #path('/<int:id>/', views., name=''),
];
