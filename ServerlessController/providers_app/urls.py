from django.urls import path

from . import views

app_name = 'providers_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('stop/', views.stop_providing, name='stop_providing'),
    path('ready/', views.ready, name='ready'),
    path('not_ready/', views.not_ready, name='not_ready'),
    path('job_ack/', views.job_ack, name='job_ack'),
]