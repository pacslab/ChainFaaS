from django.urls import path

from . import views

app_name = 'developers_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('new_service/', views.new_service, name='new_service'),
    path('user_services/', views.user_services, name='user_services'),
    path('user_jobs/', views.user_jobs, name='user_jobs'),
    path('<int:service_id>/stop_service/', views.stop_service, name='stop_service'),
    path('<int:service_id>/start_service/', views.start_service, name='start_service'),
    path('<int:service_id>/delete_service/', views.delete_service, name='delete_service'),
    path('<int:service_id>/run/', views.run_service, name='run_service'),
]