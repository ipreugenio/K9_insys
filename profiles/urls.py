from django.urls import path
from django.conf.urls import include, url
from .import views
from django.contrib.auth import views as auth_views

app_name='profiles'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('add_User_form/', views.add_User, name='add_User_form'),
    path('add_personal_form/', views.add_personal_info, name='add_personal_form')
    #path('/<int:id>/', views., name=''),
    #path('logout/', auth_views.logout, name='logout'),
    
];