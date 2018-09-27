from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='profiles'
urlpatterns = [
    path('', views.index, name='index'),
    #path('/<int:id>/', views., name=''),
];