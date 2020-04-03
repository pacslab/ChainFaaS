from django.urls import path

from . import views

app_name = 'controller_app'

urlpatterns = [
    path('job_status/', views.job_status, name='job_status'),
    # path('delete_all_jobs/', views.delete_all_jobs, name='delete_all_jobs'),
]