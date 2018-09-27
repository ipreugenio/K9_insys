from django.urls import path
from django.conf.urls import include, url
from .import views

app_name='profiles'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    #path('/<int:id>/', views., name=''),
];