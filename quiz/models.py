from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
  name = models.CharField(max_length=15)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = 'Categories'

class Quiz(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField()
  category = models.ForeignKey(Category,on_delete=models.CASCADE)
  quizfile = models.FileField(upload_to='quiz/')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.title
  
  def save(self,*args,**kwargs):
    super().save(*args,**kwargs)
    if self.quizfile:
      self.importFromExcel()
  
  def importFromExcel(self):
    import pandas as pd 
    data = pd.read_excel(self.quizfile, header=0)
    print(data)

    for index, row in data.iterrows():
        questionText = row['Questions']
        Choice1 = row['A']
        Choice2 = row['B']
        Choice3 = row['C']
        Choice4 = row['D']
        correctAns = row['Answers']

        questionObj = Question.objects.create(quiz=self, text=questionText)
        choiceObj1 = Choice.objects.create(question=questionObj, text=Choice1, isCorrect=(Choice1 == correctAns))
        choiceObj2 = Choice.objects.create(question=questionObj, text=Choice2, isCorrect=(Choice2 == correctAns))
        choiceObj3 = Choice.objects.create(question=questionObj, text=Choice3, isCorrect=(Choice3 == correctAns))
        choiceObj4 = Choice.objects.create(question=questionObj, text=Choice4, isCorrect=(Choice4 == correctAns))

  class Meta:
    verbose_name_plural = 'Quizzes'

class Question(models.Model):
  quiz = models.ForeignKey(Quiz,related_name='question',on_delete=models.CASCADE)
  text = models.TextField()

  def __str__(self):
    return self.text

class Choice(models.Model):
  question = models.ForeignKey(Question,related_name='choice',on_delete=models.CASCADE)
  text = models.TextField()
  isCorrect = models.BooleanField(default=False)

  def __str__(self):
    return self.text

class QuizSubmission(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  quiz = models.ForeignKey(Quiz,on_delete=models.CASCADE)
  score = models.IntegerField(null=True,blank=True)
  submitted_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.user} {self.quiz.title}"

class UserRank(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE)
  rank = models.IntegerField(null=True,blank=True)
  totalScore = models.IntegerField(null=True,blank=True)

  def __str__(self):
    return f"{self.user.username} {self.rank}"

@receiver(post_save,sender=QuizSubmission)
def updateLead(sender,instance,created,**kwargs):
  if created:
    update_leaderBoard()


def update_leaderBoard():
    user_scores = QuizSubmission.objects.values('user').annotate(total_score=Sum('score')).order_by('-total_score')
    rank = 1
    for item in user_scores:
        user_id = item['user']
        total_score = item['total_score']
        user = User.objects.get(pk=user_id)  # Retrieve User instance
        user_rank_obj, created = UserRank.objects.get_or_create(user=user)
        user_rank_obj.rank = rank
        user_rank_obj.totalScore = total_score
        user_rank_obj.save()
        rank += 1
  