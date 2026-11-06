
from django import forms
from .models import Application, Interview


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

        widgets = {
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your cover letter here...'
            })
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        if resume:
            if not resume.name.lower().endswith('.pdf'):
                raise forms.ValidationError(
                    'Only PDF resumes are allowed.'
                )

            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'Resume size must not exceed 5 MB.'
                )

        return resume


class InterviewForm(forms.ModelForm):

    class Meta:
        model = Interview
        fields = [
            'scheduled_at',
            'location_or_link',
            'instructions'
        ]

        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }, format='%Y-%m-%dT%H:%M'),

            'location_or_link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter office address or meeting link'
            }),

            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter interview instructions (optional)'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['scheduled_at'].input_formats = [
            '%Y-%m-%dT%H:%M'
        ]
