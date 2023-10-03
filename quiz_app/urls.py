from django.urls import path
from . import views

urlpatterns = [
    path('api/questions/', views.QuestionListCreateView.as_view(), name='question-list-create'),
    path('api/quizresults/', views.save_quiz_result, name='save-quiz-result'),
    path('api/userstats/', views.get_user_stats, name='user-stats'),
]
