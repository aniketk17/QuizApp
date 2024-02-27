from django.urls import path
from .views import*

urlpatterns = [
  path('',home,name="homepage"),
  path('home/',home,name="homepage"),
  path('all-quiz/',allquiz,name="allquizpage"),
]