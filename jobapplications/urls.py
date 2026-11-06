
from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('manage/<int:job_id>/', views.manage_applications, name='manage_applications'),
    path('update-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    path('candidate-dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('withdraw/<int:application_id>/', views.withdraw_application, name='withdraw_application'),
    path('view-candidate/<int:application_id>/', views.view_candidate_profile, name='view_candidate_profile'),

    # Interview routes
    path('schedule-interview/<int:application_id>/', views.schedule_interview, name='schedule_interview'),
    path('my-interviews/', views.my_interviews, name='my_interviews'),
    path('reschedule-interview/<int:interview_id>/', views.reschedule_interview, name='reschedule_interview'),
    path('cancel-interview/<int:interview_id>/', views.cancel_interview, name='cancel_interview'),
]
