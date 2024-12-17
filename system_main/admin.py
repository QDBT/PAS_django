from django.contrib import admin
from .models import File,AskAIRecord,DebugRecord
# Register your models here.

admin.site.register(File)
admin.site.register(AskAIRecord)
admin.site.register(DebugRecord)