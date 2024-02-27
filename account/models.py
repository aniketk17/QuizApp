from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE)
  email_address = models.EmailField(max_length=50,null=True,unique=True)
  bio = models.TextField(null=True,blank=True)
  profile_img = models.ImageField(upload_to='profile_images',default='user.png',blank=True)
