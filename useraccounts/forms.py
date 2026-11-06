
from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput()
    )

    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]


class CandidateProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
            'full_name',
            'phone',
            'location',
            'skills',
            'education',
            'summary',
            'profile_picture'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your location'
            }),

            'skills': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Python, Django, React, SQL...'
            }),

            'education': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your education details'
            }),

            'summary': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write a short professional summary'
            }),

            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
