from django.shortcuts import render
from account.models import Profile
from django.contrib.auth.models import User
def home(request):

  if request.user.is_authenticated:
    login_user = User.objects.get(username=request.user.username)
    login_profile = Profile.objects.get(user=login_user)
    context = {'login_profile':login_profile}

  else:
    context={}
  return render(request,'home.html',context)
