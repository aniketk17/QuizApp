from django.shortcuts import render
from account.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from account.models import Profile
from quiz.models import UserRank,Quiz,QuizSubmission,Question
import datetime,math
from .models import Message
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

@login_required(login_url='login_page')
def home(request):
    leaderboard_users = UserRank.objects.order_by('rank')[0:4]
    context = {'leaderboard_users':leaderboard_users}
    if request.user.is_authenticated:
        try:
            login_user = User.objects.get(username=request.user.username)
            login_profile = Profile.objects.get(user=login_user)
            context['login_profile'] = login_profile
        except User.DoesNotExist:
            return redirect('login_page')
        except Profile.DoesNotExist:
            pass
    return render(request, 'home.html', context)

def leaderboardView(request):
    leaderboard_users = UserRank.objects.order_by('rank')[0:4]

    user_obj = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_obj)

    context = {"leaderboard_users":leaderboard_users,"login_user":user_obj,"login_profile":user_profile}
    return render(request,"leaderboard.html",context)

def is_staff(user):
    return user.is_staff
    
@user_passes_test(is_staff)
@login_required(login_url='login_page')
def dashboard_view(request):
    user_obj = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_obj)
    
    total_users = User.objects.all().count()
    total_quizzes = Quiz.objects.all().count()
    total_quizz_submit = QuizSubmission.objects.all().count()
    total_questions = Question.objects.all().count()

    today_users = User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_objs = Quiz.objects.filter(created_at=datetime.date.today())
    today_quizzes = Quiz.objects.filter(created_at=datetime.date.today()).count()
    today_quiz_submit = QuizSubmission.objects.filter(submitted_at=datetime.date.today()).count()
    today_questions = 0
    for quiz in today_quizzes_objs:
        today_questions+=quiz.question.count()
    print(today_questions)
    
    gain_users = gain_percentage(total_users,today_users)
    gain_quizzes = gain_percentage(total_quizzes,today_quizzes)
    gain_quiz_submit = gain_percentage(total_quizz_submit,today_quiz_submit)
    gain_quiz_questions = gain_percentage(total_questions,today_questions)
    

    messages = Message.objects.filter(created_at__date=timezone.now().date()).order_by('-created_at')
    print(messages)
    print(Message.objects.all())
    
    context = {'login_profile':user_profile,"total_users":total_users,"total_quizzes":total_quizzes,"total_quiz_submit":total_quizz_submit,"total_questions":total_questions,
    "today_users":today_users,
    "today_quizzes":today_quizzes,
    "today_quiz_submit":today_quiz_submit,
    "today_questions":today_questions,
    "gain_users":gain_users,
    "gain_quizzes":gain_quizzes,
    "gain_quiz_submit":gain_quiz_submit,
    "gain_quiz_questions":gain_quiz_questions,
    "messages":messages}
    return render(request,'dashboard.html',context)

def gain_percentage(total,today):
    
    if total > 0 and today > 0:
        gain = math.floor((today*100)/total)
        return gain
    return 0

def about_view(request):
    
    context = {}
    if request.user.is_authenticated:
        login_user = User.objects.get(username=request.user.username)
        login_profile = Profile.objects.get(user=login_user)
        context['login_profile'] = login_profile
    return render(request,'about.html',context)

@login_required(login_url='login_page')
def contact_view(request):
    
    login_user = User.objects.get(username=request.user.username)
    login_profile = Profile.objects.get(user=login_user)
    context = {'login_profile':login_profile}
    
    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if subject is not None and message is not None:
            form = Message.objects.create(user=request.user,subject=subject,message=message)
            form.save()
            messages.success(request,"We got your message.We will resolve your query soon")
            return redirect('profile_page',request.user.username)
        else:
            return redirect('contact_page')
    
    return render(request,'contact.html')
    
@user_passes_test(is_staff)
@login_required(login_url='login')
def message_view(request,id):
    login_user = User.objects.get(username=request.user.username)
    login_profile = Profile.objects.get(user=login_user)
    message = Message.objects.filter(id=id).first()
    
    if not message.is_read:
        message.is_read = True
        message.save()
    context = {'login_profile':login_profile,'message':message}
    
    return render(request,'message.html',context)

def search_users(request):
    context = {}
    if request.user.is_authenticated:
        login_user = User.objects.get(username=request.user.username)
        login_profile = Profile.objects.get(user=login_user)
        context['login_profile'] = login_profile
    
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query)).order_by('-date_joined')
    else:
        users = []
        
    context['query'] = query
    context['leaderboard_users'] = users
    
    return render(request,"search_users.html",context)