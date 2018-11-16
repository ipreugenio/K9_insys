from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='training'
urlpatterns = [
    path('', views.index, name='index'),
    path('list-classify-k9', views.classify_k9_list, name='classify_k9_list'),
    path('classify-k9/<int:id>', views.classify_k9_select, name='classify_k9_select'),
    path('training-record', views.training_records, name='training_records'),
    path('k9-skill-classifier/', views.K9_skill_classifier, name='k9_skill_classifier'),
    path('genealogy/', views.genealogy, name='genealogy'),
    path('assign-k9/<int:id>', views.assign_k9_select, name='assign_k9_select'),
    path('training-update/<int:id>', views.training_update_form, name='training_update_form'),
    path('training-finalization/<int:id>', views.serial_number_form, name='serial_number_form'),
    path('training-details/<int:id>', views.training_details, name='training_details'),
    path('fail-dog/<int:id>', views.fail_dog, name='fail_dog'),
    path('adoption-list', views.adoption_list, name='adoption_list'),
    path('adoption-form/<int:id>', views.adoption_form, name='adoption_form'),
    path('confirm-adoption/<int:id>', views.confirm_adoption, name='confirm_adoption'),
    path('adoption-confirmed', views.adoption_confirmed, name='adoption_confirmed'),
    path('adoption-details/<int:id>', views.adoption_details, name='adoption_details'),
    #path('/<int:id>/', views., name=''),
];