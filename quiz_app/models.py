from django.db import models

class Question(models.Model):
    QUESTION_TYPES = (
        ('single', 'Single Answer'),
        ('multi', 'Multi Answer'),
    )
    
    text = models.CharField(max_length=300)
    choice_a = models.CharField(max_length=100, blank=True, null=True)
    choice_b = models.CharField(max_length=100, blank=True, null=True)
    choice_c = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=10, choices=QUESTION_TYPES, default='single')
    answers = models.CharField(max_length=300, blank=True)  # Will use | separated values for multiple answers
    lesson_name=models.CharField(max_length=300)
    
    def score_answer(self, given_answer):
        correct_answers = self.answers.split('|')
    
    # For single answer questions
        if self.type == 'single':
          
            return 1.0 if given_answer in correct_answers else 0.0
    
    # For multi-answer questions
        else:
            
        # Check if given_answer is already a list or split it
            if not isinstance(given_answer, list):
                given_answer = given_answer.split('|')
            
            correct_given = [answer for answer in given_answer if answer in correct_answers]
            a1=0
            for i in given_answer:
                if i in correct_answers:
                    a1=(1/len(correct_answers))+a1
                else:
                    
                    a1=a1-(1/len(correct_answers))
            return a1
        
    

    
    def __str__(self):
        return self.text

class QuizResult(models.Model):
    user = models.CharField(max_length=100)
    score = models.FloatField()  # Changed to FloatField to support partial scores
    total_question = models.PositiveIntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.score}/{self.total_question} - {self.date_taken}'
