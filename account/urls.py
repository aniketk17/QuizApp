from django.urls import path
from .views import*

urlpatterns = [
  path('login/',login_page,name="login_page"),
  path('register/',register_page,name="register_page"),
  path('logout/',logout_page,name="logout_page"),
  path('edit-profile/<str:username>/',edit_profile,name="editprofile_page"),
  path('delete-profile/',delete_profile,name="confirm_page"),
  path('profile/<str:username>/',profile_page,name="profile_page"),
]