# Generated by Django 4.2.5 on 2023-10-01 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz_app', '0005_alter_question_answers_alter_quizresult_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quizresult',
            name='total_questions',
        ),
    ]
