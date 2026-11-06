
from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'company',
            'location',
            'description',
            'salary'
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job title'
            }),

            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter job location'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the job requirements'
            }),

            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter salary'
            })
        }
