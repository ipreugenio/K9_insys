from django.urls import path
from django.conf.urls import include, url
from .import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user', views.UserView)


app_name='profiles'
urlpatterns = [
    path('team-leader-dashboard/', views.team_leader_dashboard, name='team_leader_dashboard'),
    path('handler-dashboard/', views.handler_dashboard, name='handler_dashboard'),
    path('vet-dashboard/', views.vet_dashboard, name='vet_dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('notifications/', views.notif_list, name='notif_list'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html') ,name='login'),
    #path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('add_User_form/', views.add_User, name='add_User_form'),
    path('add_User_form/add_personal_form/', views.add_personal_info, name='add_personal_form'),
    path('add_User_form/add_personal_form/add_education/', views.add_education, name='add_education'),
    path('add_User_form/add_personal_form/add_education/add_user_account/', views.add_account, name='add_user_account'),
    path('user_list/', views.user_listview, name='user_list'),
    path('user_detail/<int:id>', views.user_detailview, name='user_detail'),
    path('user_add_confirmed/', views.user_add_confirmed, name='user_add_confirmed'),

    path('api', views.NotificationListView.as_view()),
    path('api/<int:id>', views.NotificationDetailView.as_view()),

    # path('user/api', views.UserListView.as_view()),
    # path('user/api/<int:id>', views.UserDetailView.as_view()),

    path('user/api', include(router.urls)),

];