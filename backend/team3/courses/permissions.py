from django.shortcuts import get_object_or_404
from rest_framework import permissions

from . import views
from .models import Course, ArticleModel, CommentModel


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True


class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_anonymous and request.user.is_teacher


class IsTeacherOrReadOnly(IsTeacher):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return super().has_permission(request, view)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Course):
            return obj.teacher == request.user
        elif isinstance(obj, ArticleModel) or isinstance(obj, CommentModel):
            return obj.author == request.user
        else:
            return False


# ArticleList, ArticleDetail, CommentList, CommentDetail, CourseDetail
class IsMemberOfCourseOrNotAllowed(permissions.BasePermission):
    message = "You are not member of this course"

    def has_permission(self, request, view):
        id = self.get_course_id(view)
        return self.is_member(request.user, id)

    def has_object_permission(self, request, view, obj):
        id = self.get_course_id(view)
        return self.is_member(request.user, id)

    def get_course_id(self, view):
        id = 0
        if isinstance(view, views.CourseDetail) or isinstance(view, views.ArticleList) \
                or isinstance(view, views.RecentArticle):
            id = view.kwargs['pk']
        elif isinstance(view, views.CommentList) or isinstance(view, views.CommentDetail):
            id = get_object_or_404(ArticleModel, pk=view.kwargs['article_id']).course_id
        elif isinstance(view, views.ArticleSearch):
            id = view.kwargs['course_id']
        else:
            # ArticleDetail
            id = get_object_or_404(ArticleModel, pk=view.kwargs['pk']).course_id
        return id

    def is_member(self, user, id):
        courses = user.teacher_course.all() if user.is_teacher else user.students_course.all()
        for course in courses:
            if course.id == id:
                return True
        return False


class NotYetApplied(permissions.BasePermission):
    message = "You already applied for this course."

    def has_object_permission(self, request, view, obj):
        return len(obj.students.filter(id=request.user.id)) is 0


class IsStudent(permissions.BasePermission):
    message = "Teacher can not apply for course"

    def has_object_permission(self, request, view, obj):
        return not request.user.is_teacher
