from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from rest_framework import generics
# Create your views here.


from . import models
from . import serializers
from . import permissions


class QuizBox(generics.RetrieveAPIView):
    queryset = models.QuizBox.objects.all()
    serializer_class = serializers.QuizBoxSerializer
    lookup_url_kwarg = 'box_id'
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated, permissions.IsCourseMember, )


class Quiz(generics.ListCreateAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated, permissions.IsCourseMemberForList, permissions.IsCourseOwnerOrReadOnly, )

    def get_queryset(self):
        box_id = self.kwargs.get('box_id')
        return super().get_queryset().filter(quizbox__id=box_id)

    def get_serializer_context(self):
        context = {'box_id': self.kwargs.get('box_id')}
        return context


class QuizDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuizDetailSerializer
    pagination_class = None
    lookup_url_kwarg = 'quiz_id'
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated, permissions.IsCourseMember, permissions.IsCourseOwnerOrReadOnly)


class Question(generics.ListCreateAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated, permissions.IsCourseMemberForList, )

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        return super().get_queryset().filter(quiz__id=quiz_id)

    def get_serializer_context(self):
        context = {'quiz_id': self.kwargs.get('quiz_id')}
        return context


class QuestionAll(generics.RetrieveUpdateAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.QuestionAllSerializer
    lookup_url_kwarg = 'quiz_id'

    def get_serializer_context(self):
        context = {'quiz_id': self.kwargs.get('quiz_id')}
        return context



class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.QuestionDetailSerializer
    pagination_class = None
    lookup_url_kwarg = 'question_id'
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated, permissions.IsCourseMember, )


class AnswerAppend(generics.CreateAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerAppendSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'question_id': self.kwargs.get('question_id')})
        return context


class AnswerDelete(generics.DestroyAPIView):
    queryset = models.Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    lookup_url_kwarg = 'answer_id'
    lookup_field = 'id'


class AllStudentsGrade(generics.ListAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.AllStudentGradeSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated, permissions.IsCourseOwnerOrNotAllowed, )

    def get_queryset(self):
        quiz_id = self.kwargs.get('quiz_id')
        return super().get_queryset().filter(quiz__id=quiz_id)


class MyGradeBox(generics.RetrieveAPIView):
    queryset = models.GradeBox.objects.all()
    serializer_class = serializers.MyGradeBoxSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class MyQuizGradeBox(generics.ListAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.MyGradeSerializer
    pagination_class = None
    permission_classes = (permissions.IsAuthenticated, permissions.IsCourseMemberForList)

    def get_queryset(self):
        return super().get_queryset().filter(quiz__quizbox__course__id=self.kwargs.get('course_id'), gradebox__user=self.request.user)


class GradeQuestion(generics.RetrieveUpdateAPIView):
    queryset = models.Question.objects.all()
    serializer_class = serializers.GradeQuestionSerializer
    lookup_url_kwarg = 'question_id'
    permission_classes = (permissions.IsAuthenticated, permissions.IsCourseMember, )


class GradeQuiz(generics.RetrieveUpdateAPIView):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeQuizSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsCourseMember, permissions.DueIsOver, permissions.IsNotSubmitted)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), gradebox__user=self.request.user, quiz__id=self.kwargs.get('quiz_id'))
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_context(self):
        return {'quiz_id': self.kwargs.get('quiz_id')}


class UpcomingQuiz(generics.ListAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.UpcomingQuizSerializer

    def get_queryset(self):
        now = timezone.localtime()
        query = super().get_queryset()
        return query.filter(due__gt=now)


class UpcomingQuizAll(generics.ListAPIView):
    queryset = models.Quiz.objects.all()
    serializer_class = serializers.UpcomingQuizAllSerializer

    def get_queryset(self):
        courses = self.request.user.students_course.all()
        query =super().get_queryset()
        _from = timezone.localtime()
        _to = _from + timezone.timedelta(days=7)
        res = models.Quiz.objects.none()
        for c in courses:
            res |= query.filter(quizbox__course=c).filter(due__gt=_from, due__lte=_to)
        return res

