from django import forms
from .models import CodeSnippet,CodeRecord

# Form for the main writing Code
class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['code']
        widgets = {
            'code': forms.Textarea(attrs={'class': 'codemirror'}),
        }

# Form for creating a new Snippet
class CreateSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['title']
        widgets = {
            'title':forms.Textarea(attrs={'placeholder':''}),
        }

class CodeRecordForm(forms.ModelForm):
    class Meta:
        model = CodeRecord
        fields = ['original_code']