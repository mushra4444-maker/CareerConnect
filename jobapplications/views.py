
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.files.storage import default_storage

from jobportal.models import Job
from .models import Application, Interview
from .forms import ApplicationForm, InterviewForm


@login_required
def apply_job(request, job_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'candidate':
        return render(request, 'unauthorized.html')

    job = get_object_or_404(Job, id=job_id, is_active=True)

    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_list')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()

            messages.success(request, 'Your application was submitted successfully!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'apply_job.html', {'form': form, 'job': job})


@login_required
def my_applications(request):
    applications = Application.objects.filter(
        candidate=request.user
    ).select_related('job').order_by('-applied_at')

    return render(request, 'my_applications.html', {
        'applications': applications
    })


@login_required
def manage_applications(request, job_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    job = get_object_or_404(Job, id=job_id, employer=request.user)

    search_query = request.GET.get('q', '').strip()
    selected_status = request.GET.get('status', '').strip()

    applications = Application.objects.filter(
        job=job
    ).select_related('candidate').order_by('-applied_at')

    if search_query:
        applications = applications.filter(
            candidate__username__icontains=search_query
        )

    valid_statuses = [
        'pending', 'reviewed', 'shortlisted', 'rejected', 'accepted'
    ]

    if selected_status in valid_statuses:
        applications = applications.filter(status=selected_status)
    else:
        selected_status = ''

    context = {
        'job': job,
        'applications': applications,
        'search_query': search_query,
        'selected_status': selected_status,
        'total_applications': Application.objects.filter(job=job).count(),
    }

    return render(request, 'manage_applications.html', context)


@login_required
@require_POST
def update_application_status(request, application_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user
    )

    new_status = request.POST.get('status')

    valid_statuses = [
        'pending', 'reviewed', 'shortlisted', 'rejected', 'accepted'
    ]

    if new_status in valid_statuses:
        application.status = new_status
        application.save(update_fields=['status'])
        messages.success(request, 'Application status updated successfully!')
    else:
        messages.error(request, 'Invalid application status!')

    return redirect('manage_applications', job_id=application.job.id)


@login_required
def candidate_dashboard(request):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'candidate':
        return render(request, 'unauthorized.html')

    applications = Application.objects.filter(
        candidate=request.user
    ).select_related('job').order_by('-applied_at')

    context = {
        'applications': applications,
        'total_applications': applications.count(),
        'pending_count': applications.filter(status='pending').count(),
        'reviewed_count': applications.filter(status='reviewed').count(),
        'shortlisted_count': applications.filter(status='shortlisted').count(),
        'accepted_count': applications.filter(status='accepted').count(),
        'rejected_count': applications.filter(status='rejected').count(),
    }

    return render(request, 'candidate_dashboard.html', context)


@login_required
@require_POST
def withdraw_application(request, application_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'candidate':
        return render(request, 'unauthorized.html')

    application = get_object_or_404(
        Application,
        id=application_id,
        candidate=request.user
    )

    if application.status != 'pending':
        messages.error(request, 'Only pending applications can be withdrawn.')
        return redirect('candidate_dashboard')

    if application.resume:
        if default_storage.exists(application.resume.name):
            default_storage.delete(application.resume.name)

    application.delete()

    messages.success(
        request,
        'Your job application has been withdrawn successfully.'
    )

    return redirect('candidate_dashboard')


@login_required
def view_candidate_profile(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if application.job.employer != request.user:
        return render(request, 'unauthorized.html')

    candidate = application.candidate

    if not hasattr(candidate, 'userprofile'):
        return render(request, 'unauthorized.html')

    profile = candidate.userprofile

    return render(request, 'view_candidate_profile.html', {
        'application': application,
        'candidate': candidate,
        'profile': profile,
    })


@login_required
def schedule_interview(request, application_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user
    )

    if request.method == 'POST':
        form = InterviewForm(request.POST)

        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()

            messages.success(request, 'Interview scheduled successfully!')

            return redirect(
                'manage_applications',
                job_id=application.job.id
            )
    else:
        form = InterviewForm()

    return render(request, 'schedule_interview.html', {
        'form': form,
        'application': application,
    })


@login_required
def reschedule_interview(request, interview_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    interview = get_object_or_404(
        Interview,
        id=interview_id,
        application__job__employer=request.user
    )

    if interview.status == 'cancelled':
        messages.error(request, 'Cancelled interviews cannot be rescheduled.')
        return redirect(
            'manage_applications',
            job_id=interview.application.job.id
        )

    if request.method == 'POST':
        form = InterviewForm(request.POST, instance=interview)

        if form.is_valid():
            form.save()

            messages.success(request, 'Interview rescheduled successfully!')

            return redirect(
                'manage_applications',
                job_id=interview.application.job.id
            )
    else:
        form = InterviewForm(instance=interview)

    return render(request, 'reschedule_interview.html', {
        'form': form,
        'interview': interview,
    })


@login_required
@require_POST
def cancel_interview(request, interview_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    interview = get_object_or_404(
        Interview,
        id=interview_id,
        application__job__employer=request.user
    )

    if interview.status == 'scheduled':
        interview.status = 'cancelled'
        interview.save(update_fields=['status'])

        messages.success(request, 'Interview cancelled successfully!')
    else:
        messages.warning(request, 'This interview is already cancelled.')

    return redirect(
        'manage_applications',
        job_id=interview.application.job.id
    )


@login_required
def my_interviews(request):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'candidate':
        return render(request, 'unauthorized.html')

    interviews = Interview.objects.filter(
        application__candidate=request.user
    ).select_related(
        'application',
        'application__job',
        'application__job__employer'
    ).order_by('scheduled_at')

    return render(request, 'my_interviews.html', {
        'interviews': interviews
    })
