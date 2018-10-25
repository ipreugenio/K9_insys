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
    
    #path('/<int:id>/', views., name=''),
];