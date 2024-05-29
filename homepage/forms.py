from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_at', 'program_language']
        widgets = {
            'start_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }