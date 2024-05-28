from django.contrib import admin
from .models import User,Session,Message,CodeSnippet,CodeFixSuggestion

admin.site.register(User)
admin.site.register(Session)
admin.site.register(Message)
admin.site.register(CodeSnippet)
admin.site.register(CodeFixSuggestion)
# Register your models here.
