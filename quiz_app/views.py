# Create your views here.
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Question, QuizResult
from .serializers import QuestionSerializer, QuizResultSerializer
from django.db.models import Count, Avg

class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

@api_view(['GET'])
def get_user_stats(request):
    user_stats = QuizResult.objects.values('user').annotate(
        attempted=Count('user'),
        average_score=Avg('score')
    )
    return Response(user_stats, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_quiz_result(request):
    if request.method == 'POST':
        # Extract the answers given by the user
        user_answers = request.data.get('answers', {})
        total_question = len(user_answers)
        

        # Calculate the score based on the answers
        score = 0.0
        a2=[]
        for question_id, given_answer in user_answers.items():
            try:
                question = Question.objects.get(pk=question_id)
                if question.score_answer(given_answer) > 0:  
                    a2.append(question.score_answer(given_answer))
                    
            except Question.DoesNotExist:
                return Response({'error': f'Question with id {question_id} does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)

        
        total_question = Question.objects.all().count()
        if len(a2)==0:
            a2.append(0.0)
        result_data = {
    'user': request.data.get('user'),
    'score': sum(a2),
    'total_question':total_question
     }
        


        serializer = QuizResultSerializer(data=result_data)
        user_stats = QuizResult.objects.values('user').annotate(
        attempted=Count('user'),
        average_score=Avg('score')
        )
       

        if serializer.is_valid():
            serializer.save()
            return Response({'score': sum(a2),'total_question':total_question}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

