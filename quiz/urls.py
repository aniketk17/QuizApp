from django.urls import path
from .views import*

urlpatterns = [
  path('quiz/<int:id>',quiz,name="quizPage"),
  path('all-quiz/',allquiz,name="allquizpage"),
  path('search-quiz/<str:category>',search_quiz,name="searchQuiz"),
  path('SearchQuiz/',searchQuizBySearchBar,name="searchBySearchBar"),
]