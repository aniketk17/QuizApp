from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from account.models import Profile
from .models import *
from django.db.models import Q

def quiz(request):
  return render(request,'quiz.html')

@login_required(login_url='login_page')
def allquiz(request):
  user_model = User.objects.get(username=request.user.username)
  profile_model = Profile.objects.get(user=user_model)
  quizzes = Quiz.objects.order_by("-created_at")
  quizCategory = Category.objects.all()
  context = {'login_user':user_model,'login_profile':profile_model,'quizzes':quizzes,'categories':quizCategory}
  return render(request,'all-quiz.html',context)

def search_quiz(request, category):
    user_model = User.objects.get(username=request.user.username)
    profile_model = Profile.objects.get(user=user_model)

    if category != "":
        quizzes = Quiz.objects.filter(category__name=category)
        print(category)
    elif request.method == "GET" and 'q' in request.GET:
        q = request.GET.get('q')
        print("get")
        quizzes = Quiz.objects.filter(Q(title__icontains=q) | Q(description__icontains=q)).distinct()
        print(quizzes)
    else:
        quizzes = Quiz.objects.order_by("-created_at")

    quizCategory = Category.objects.all()
    context = {'login_user': user_model, 'login_profile': profile_model, 'quizzes': quizzes, 'categories': quizCategory}
    return render(request, 'all-quiz.html', context)