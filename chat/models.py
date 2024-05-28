from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

class Message(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_text = models.TextField()
    message_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

class CodeSnippet(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_code = models.TextField()
    fixed_code = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    fixed_at = models.DateTimeField(null=True, blank=True)

class CodeFixSuggestion(models.Model):
    snippet = models.ForeignKey(CodeSnippet, on_delete=models.CASCADE)
    suggestion_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)