import datetime

from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, UpdateAPIView, \
    get_object_or_404, RetrieveAPIView, GenericAPIView
# from django_filters import rest_framework as filters
from rest_framework import filters

from datetime import date

from .models import Course, ArticleModel, CommentModel
from .models import IS_NOTICE, IS_REFERENCE, IS_QNA
from .serializers import CourseSerializer, ArticleSerializer, NoticeSerializer, ReferenceSerializer, QnASerializer, \
    CommentSerializer, ArticleDetailSerializer, CourseApplySerializer, CommentDetailSerializer, CourseDetailSerializer, \
    RecentArticleSerializer, TeacherNoticeSerializer, TeacherArticleDetailSerializer
from .permissions import IsTeacherOrReadOnly, IsOwnerOrReadOnly, IsMemberOfCourseOrNotAllowed, NotYetApplied, IsStudent

# Create new course and list courses
class CourseList(ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsTeacherOrReadOnly, )


# Update, delete, get detail course
class CourseDetail(RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = (IsOwnerOrReadOnly, IsMemberOfCourseOrNotAllowed)


# Create new article related to specific course, list articles
class ArticleList(ListCreateAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (IsMemberOfCourseOrNotAllowed, )

    def get_queryset(self):
        return super().get_queryset().filter(course__id=self.kwargs.get('pk')).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'course_id': self.kwargs['pk']})
        return context

class NoticeArticle(ArticleList):
    queryset = ArticleModel.objects.filter(type=IS_NOTICE)
    serializer_class = NoticeSerializer

    def get_queryset(self):
        return super().get_queryset().filter(course__id=self.kwargs.get('pk')).order_by('-important').order_by('-created_at')

    def get_serializer_class(self):
        if self.request.user.is_teacher:
            return TeacherNoticeSerializer
        return super().get_serializer_class()

class ReferenceArticle(ArticleList):
    queryset = ArticleModel.objects.filter(type=IS_REFERENCE)
    serializer_class = ReferenceSerializer

    def get_queryset(self):
        return super().get_queryset().filter(course__id=self.kwargs.get('pk')).order_by('-created_at')


class QnAArticle(ArticleList):
    queryset = ArticleModel.objects.filter(type=IS_QNA)
    serializer_class = QnASerializer

    def get_queryset(self):
        return super().get_queryset().filter(course__id=self.kwargs.get('pk')).order_by('-created_at')


class ArticleDetail(RetrieveUpdateDestroyAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = (IsMemberOfCourseOrNotAllowed, IsOwnerOrReadOnly, )

    def get_serializer_class(self):
        if self.request.user.is_teacher:
            return TeacherArticleDetailSerializer
        return super().get_serializer_class()

# Comments
class CommentList(ListCreateAPIView):
    queryset = CommentModel.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsMemberOfCourseOrNotAllowed, )
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(article__id=self.kwargs.get('article_id')).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'article_id': self.kwargs['article_id']})
        return context


class CommentDetail(RetrieveUpdateDestroyAPIView):
    queryset = CommentModel.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = (IsOwnerOrReadOnly, IsMemberOfCourseOrNotAllowed)


# class CourseApply(UpdateAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseApplySerializer
#     lookup_field = 'id'
#     lookup_url_kwarg = 'course_id'


class CourseApply(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseApplySerializer
    permission_classes = (IsStudent, NotYetApplied, )

    def get_object(self):
        uuid = self.request.data.get('uuid')
        obj = get_object_or_404(self.get_queryset(), uuid=uuid)
        self.check_object_permissions(self.request, obj)
        return obj


class Recent(ListAPIView):
    serializer_class = RecentArticleSerializer
    display = 7

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_teacher:
            courses = user.teacher_course.all()
            # query = super().get_queryset().filter(teacher=user)
        else:
            courses = user.students_course.all()
            # query = super().get_queryset().filter(students=user)
        query = ArticleModel.objects.none()
        for course in courses:
            query |= course.articlemodel_set.all()
        return query.filter(type=IS_NOTICE).order_by('-created_at')[:self.display]

class RecentArticle(ListAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = RecentArticleSerializer
    permission_classes = (IsMemberOfCourseOrNotAllowed, )
    display = 7

    def get_queryset(self):
        # _from = date.today()
        # _to = _from + datetime.timedelta(7)
        # return super().get_queryset().filter(course__id=self.kwargs.get('pk')).filter(created_at__range=[_from, _to])
        return super().get_queryset().filter(course__id=self.kwargs.get('pk')).order_by('-created_at')[:self.display]

class RecentNoticeArticle(RecentArticle):
    queryset = ArticleModel.objects.filter(type=IS_NOTICE)

class RecentReferenceArticle(RecentArticle):
    queryset = ArticleModel.objects.filter(type=IS_REFERENCE)

class RecentQnAArticle(RecentArticle):
    queryset = ArticleModel.objects.filter(type=IS_QNA)


class ArticleSearch(ListAPIView):
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('title', 'content', 'author__username')
    permission_classes = (IsMemberOfCourseOrNotAllowed, )

    def get_queryset(self):
        return super().get_queryset().filter(course__id=self.kwargs.get('course_id'))


class NoticeArticleSearch(ArticleSearch):
    queryset = ArticleModel.objects.filter(type=IS_NOTICE)
    serializer_class = NoticeSerializer


class ReferenceArticleSearch(ArticleSearch):
    queryset = ArticleModel.objects.filter(type=IS_REFERENCE)
    serializer_class = ReferenceSerializer


class QnAArticleSearch(ArticleSearch):
    queryset = ArticleModel.objects.filter(type=IS_QNA)
    serializer_class = QnASerializer
