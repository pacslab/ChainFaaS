from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('change_info/', views.change_info, name='change_info'),
    path('delete_test_users/', views.delete_test_users, name='delete_test_users'),
]