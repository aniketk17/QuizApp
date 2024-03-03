from django.db import models

class Category(models.Model):
  name = models.CharField(max_length=15)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = 'Categories'

class Quiz(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  category = models.OneToOneField(Category,on_delete=models.CASCADE)
  quizfile = models.FileField(upload_to='quiz/')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.title
    
  class Meta:
    verbose_name_plural = 'Quizzes'
