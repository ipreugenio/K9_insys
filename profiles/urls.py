from django.urls import path
from django.conf.urls import include, url
from .import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

app_name='profiles'
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notif_list, name='notif_list'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('add_User_form/', views.add_User, name='add_User_form'),
    path('add_User_form/add_personal_form/', views.add_personal_info, name='add_personal_form'),
    path('add_User_form/add_personal_form/add_education/', views.add_education, name='add_education'),
    path('add_User_form/add_personal_form/add_education/add_user_account/', views.add_account, name='add_user_account'),
    path('user_list/', views.user_listview, name='user_list'),
    path('user_detail/<int:id>', views.user_detailview, name='user_detail'),
    path('user_add_confirmed/', views.user_add_confirmed, name='user_add_confirmed'),

    path('api', views.NotificationListView.as_view()),
    path('api/<int:id>', views.NotificationDetailView.as_view()),

    #path('/<int:id>/', views., name=''),
    #path('logout/', auth_views.logout, name='logout'),
    
];