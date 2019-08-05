from django.utils import timezone

from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated

from courses.models import Course

from . import models
from . import views


class IsCourseMember(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if isinstance(obj, models.QuizBox):
            course = obj.course
        elif isinstance(obj, models.Quiz):
            course = obj.quizbox.course
        elif isinstance(obj, models.Question):
            course = obj.quiz.quizbox.course
        elif isinstance(obj, models.Grade):
            course = obj.quiz.quizbox.course
        if user.is_teacher:
            return course.teacher == user
        else:
            return len(course.students.filter(pk=user.id)) is not 0


class IsCourseMemberForList(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        course = None
        if isinstance(view, views.Quiz):
            id = view.kwargs.get('box_id')
            course = models.QuizBox.objects.get(pk=id).course
        elif isinstance(view, views.Question):
            id = view.kwargs.get('quiz_id')
            course = models.Quiz.objects.get(pk=id).quizbox.course
        elif isinstance(view, views.MyQuizGradeBox):
            id = view.kwargs.get('course_id')
            course = Course.objects.get(pk=id)
        if user.is_teacher:
            return course.teacher == user
        return len(course.students.filter(pk=user.id)) is not 0


class IsCourseOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if isinstance(view, views.Quiz):
            quizbox = models.QuizBox.objects.get(pk=view.kwargs.get('box_id'))
        elif isinstance(view, views.QuizDetail):
            quizbox = models.Quiz.objects.get(pk=view.kwargs.get('quiz_id')).quizbox
        return quizbox.owner==user


class IsCourseOwnerOrNotAllowed(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        quiz_id = view.kwargs.get('quiz_id')
        quiz = models.Quiz.objects.get(pk=quiz_id)
        return quiz.quizbox.course.teacher==user


class IsNotSubmitted(permissions.BasePermission):
    message = "You already submitted quiz."

    def has_object_permission(self, request, view, obj):
        return not obj.is_submitted


class DueIsOver(permissions.BasePermission):
    message = "제출 시간이 지났습니다."

    def has_object_permission(self, request, view, obj):
        now = timezone.localtime()
        return now < obj.quiz.due
