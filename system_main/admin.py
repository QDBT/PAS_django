from django.contrib import admin
from .models import CodeSnippet,AskAIRecord,DebugRecord
# Register your models here.

admin.site.register(CodeSnippet)
admin.site.register(AskAIRecord)
admin.site.register(DebugRecord)