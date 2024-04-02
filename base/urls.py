from django.urls import path
from .views import*

urlpatterns = [
  path('',home,name="home_page"),
  path('home/',home,name="home_page"),
  path('dashboard/',dashboard_view,name="dashboard_page"),
  path('about/',about_view,name="about_page"),
  path('contact/',contact_view,name="contact_page"),
  path('message/<int:id>',message_view,name="message_page"),
  path('leaderboard/',leaderboardView,name="leaderboard_page"),
  path('search_users/',search_users,name="search_users_page"),
]