from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'language', 'description']
        widgets = { 
             'language': forms.Select(attrs={'class': 'language-select'}),
             'title':forms.TextInput(attrs={'placeholder':'Name of your project'}),
        }
