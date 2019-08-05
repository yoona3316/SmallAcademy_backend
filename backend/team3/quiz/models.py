from django.conf import settings
from django.db import models
# Create your models here.
from courses.models import Course


class QuizBox(models.Model):
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='quizbox')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quizbox_owner')

class Quiz(models.Model):
    title = models.CharField(max_length=20)
    due = models.DateTimeField()
    quizbox = models.ForeignKey(QuizBox, on_delete=models.CASCADE, related_name='quiz')

    def __str__(self):
        return self.title

class Question(models.Model):
    question = models.CharField(max_length=50)
    explanation = models.TextField(max_length=500, null=True, blank=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')


class Answer(models.Model):
    answer = models.CharField(max_length=100)
    is_answer = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

class GradeBox(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gradebox')

    def __str__(self):
        return self.user.username

class Grade(models.Model):
    grade = models.IntegerField(default=0)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='grade')
    is_submitted = models.BooleanField(default=False)
    gradebox = models.ForeignKey(GradeBox, on_delete=models.CASCADE, related_name='grades')
    wrong_answers = models.ManyToManyField(Question, related_name='wrong_answers')
