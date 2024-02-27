from django.shortcuts import render

def quiz(request):
  return render(request,'quiz.html')

def allquiz(request):
  return render(request,'all-quiz.html')