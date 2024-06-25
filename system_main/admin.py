from django.contrib import admin
from .models import CodeSnippet,CodeRecord
# Register your models here.

admin.site.register(CodeSnippet)
admin.site.register(CodeRecord)