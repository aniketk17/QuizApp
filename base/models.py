from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  subject = models.CharField(max_length=255)
  message = models.TextField()
  is_read = models.BooleanField(default=False)
  created_at = models.DateTimeField(default=timezone.now)
  
  def __str__(self):
    return f"{self.user.username},{self.subject}" 