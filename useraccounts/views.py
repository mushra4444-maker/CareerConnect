
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile
from .forms import RegisterForm, CandidateProfileForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid username or password'

    return render(request, 'login.html', {'error': error})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def candidate_profile(request):

    # Check whether the user has a profile
    if not hasattr(request.user, 'userprofile'):
        return render(request, 'unauthorized.html')

    # Only candidates can access this page
    if request.user.userprofile.role != 'candidate':
        return render(request, 'unauthorized.html')

    profile = request.user.userprofile

    if request.method == 'POST':
        form = CandidateProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your profile has been updated successfully!'
            )

            return redirect('candidate_profile')

    else:
        form = CandidateProfileForm(instance=profile)

    return render(
        request,
        'candidate_profile.html',
        {
            'form': form,
            'profile': profile
        }
    )
