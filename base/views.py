from django.shortcuts import render

def home(request):
  return render(request,'home.html')

def allquiz(request):
  return render(request,'all-quiz.html')