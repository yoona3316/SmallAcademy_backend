from rest_framework import serializers
from . import models

class NestQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        exclude = ('quizbox', )
