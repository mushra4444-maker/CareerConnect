
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from decimal import Decimal, InvalidOperation

from .models import Job
from .forms import JobForm
from jobapplications.models import Application


def home(request):
    return render(request, 'home.html')


@login_required
def post_job(request):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()

            messages.success(request, 'Job posted successfully!')
            return redirect('job_list')
    else:
        form = JobForm()

    return render(request, 'post_job.html', {'form': form})


def job_list(request):
    search_query = request.GET.get('q', '').strip()
    min_salary = request.GET.get('min_salary', '').strip()
    max_salary = request.GET.get('max_salary', '').strip()
    sort_by = request.GET.get('sort', 'newest')

    jobs = Job.objects.filter(is_active=True)

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query) |
            Q(company__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    if min_salary:
        try:
            jobs = jobs.filter(salary__gte=Decimal(min_salary))
        except InvalidOperation:
            min_salary = ''

    if max_salary:
        try:
            jobs = jobs.filter(salary__lte=Decimal(max_salary))
        except InvalidOperation:
            max_salary = ''

    if sort_by == 'oldest':
        jobs = jobs.order_by('created_at')
    else:
        sort_by = 'newest'
        jobs = jobs.order_by('-created_at')

    applied_job_ids = set()

    if request.user.is_authenticated:
        if hasattr(request.user, 'userprofile'):
            if request.user.userprofile.role == 'candidate':
                applied_job_ids = set(
                    Application.objects.filter(
                        candidate=request.user
                    ).values_list('job_id', flat=True)
                )

    paginator = Paginator(jobs, 6)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'jobs': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
        'min_salary': min_salary,
        'max_salary': max_salary,
        'sort_by': sort_by,
        'applied_job_ids': applied_job_ids,
    }

    return render(request, 'job_list.html', context)


def job_detail(request, job_id):
    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    return render(request, 'job_detail.html', {'job': job})


@login_required
def employer_dashboard(request):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    jobs = Job.objects.filter(
        employer=request.user
    ).order_by('-created_at')

    return render(request, 'employer_dashboard.html', {'jobs': jobs})


@login_required
def edit_job(request, job_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)

    return render(
        request,
        'edit_job.html',
        {'form': form, 'job': job}
    )


@login_required
@require_POST
def delete_job(request, job_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    job.delete()

    messages.success(request, 'Job deleted successfully!')
    return redirect('employer_dashboard')


@login_required
@require_POST
def toggle_job_status(request, job_id):
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    if request.user.userprofile.role != 'employer':
        return render(request, 'unauthorized.html')

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    job.is_active = not job.is_active
    job.save(update_fields=['is_active'])

    if job.is_active:
        messages.success(request, 'Job reopened successfully!')
    else:
        messages.success(request, 'Job closed successfully!')

    return redirect('employer_dashboard')
