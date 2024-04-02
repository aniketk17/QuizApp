from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import*
from django.contrib.auth.decorators import login_required


def register_page(request):

  if request.user.is_authenticated:
      return redirect('profile_page',request.user.username) 
  if request.method == "POST":
    data = request.POST
    username = data.get('username')
    email = data.get('email')
    password1 = data.get('password1')
    password2 = data.get('password2')

    if password1 == password2:
      print("passWord Math")
      if(User.objects.filter(username=username).exists()):
        messages.info(request,"username already taken")
        return redirect('register_page')
      
      elif(User.objects.filter(email=email).exists()):
        messages.info(request,"email address should be unique")
        return redirect('register_page')

      else:
        newuser = User.objects.create(
          username = username,
          email = email
        )
        newuser.set_password(password1)
        newuser.save()
        messages.info(request,"account created successfully")

        profile_model = Profile.objects.create(
          user = newuser,
        )
        login(request,newuser)
        return redirect('profile_page',username)

    else:
      messages.info(request,"Password are not matching")
  
  return render(request,'register.html')

@login_required(login_url='login_page')
def profile_page(request,username):
  if username:
    user_object = User.objects.filter(username=username).first()
    user_profile = Profile.objects.filter(user = user_object).first()

    login_user = User.objects.filter(username=request.user).first()
    login_profile = Profile.objects.filter(user = login_user).first()
    context = {'user_profile':user_profile,'login_profile':login_profile}
    return render(request,'profile.html',context)


def login_page(request):
  if request.method == "POST":
    data = request.POST
    username = data.get('username')
    password = data.get('password')

    user_model = authenticate(username=username,password=password)
    if user_model is not None:
      login(request,user_model)
      return redirect('homepage')
    else:
      messages.info(request,"Invalid Credentials")
      return redirect('login_page')

  return render(request,'login.html')

@login_required(login_url='login_page')
def logout_page(request):
  logout(request)
  return redirect('login_page')

@login_required(login_url='login_page')
def edit_profile(request, username):
    if request.user.is_authenticated:
        login_user = User.objects.filter(username=username).first()
        login_profile = Profile.objects.filter(user=login_user).first()
        
        if request.method == "POST":
            if request.FILES.get('profile_img'):
                login_profile.profile_img = request.FILES.get('profile_img')
                login_profile.save()
            
            data = request.POST
            first_name = data.get('first_name')
            if first_name:
                login_user.first_name = first_name
                login_user.save()
            
            last_name = data.get('last_name')
            if last_name:
                login_user.last_name = last_name
                login_user.save()
            
            email = data.get('email')
            if email:
                existing_user_with_email = User.objects.filter(email=email).exclude(username=username)
                if existing_user_with_email.exists():
                    messages.info(request, "Email already taken")
                    return redirect('editprofile_page', username=username)
                login_user.email = email
                login_user.save()

            new_username = data.get('username')
            if new_username:
                existing_user_with_username = User.objects.filter(username=new_username).exclude(username=username)
                if existing_user_with_username.exists():
                    messages.info(request, "Username already exists")
                    return redirect('editprofile_page', username=username)
                login_user.username = new_username
                login_user.save()
            
            bio = data.get('bio')
            if bio:
                login_profile.bio = bio
                login_profile.save()

            return redirect('profile_page', username=username)
        
        context = {'login_profile': login_profile}
        return render(request, 'profile-edit.html', context)
    else:
        return redirect('login_page')

def delete_profile(request):
  login_user = User.objects.get(username=request.user.username)
  login_profile = Profile.objects.get(user = login_user)

  if request.method == "POST":
    login_profile.delete()
    login_user.delete()
    return redirect('logout_page')
  
  context = {'login_profile':login_profile}
  return render(request,'confirm.html',context)
