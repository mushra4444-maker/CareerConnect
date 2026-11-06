
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Job posting and listing
    path('post-job/', views.post_job, name='post_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),

    # Employer dashboard
    path(
        'employer-dashboard/',
        views.employer_dashboard,
        name='employer_dashboard'
    ),

    # Edit and delete jobs
    path(
        'edit-job/<int:job_id>/',
        views.edit_job,
        name='edit_job'
    ),
    path(
        'delete-job/<int:job_id>/',
        views.delete_job,
        name='delete_job'
    ),

    # Activate and deactivate jobs
    path(
        'toggle-job-status/<int:job_id>/',
        views.toggle_job_status,
        name='toggle_job_status'
    ),
]
