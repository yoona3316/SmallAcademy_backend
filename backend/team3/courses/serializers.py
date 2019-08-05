from django.utils import timezone

from rest_framework import serializers

from accounts.nests import UserProfileSerializer

from .models import Course, ArticleModel, IS_NOTICE, IS_REFERENCE, IS_QNA, CommentModel
from quiz.models import QuizBox, Quiz, Grade

class CourseSerializer(serializers.ModelSerializer):
    _teacher = serializers.HiddenField(default=serializers.CurrentUserDefault(), source='teacher')
    teacher = serializers.StringRelatedField()
    students = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'course_name', '_teacher', 'teacher', 'students',)

    def create(self, validated_data):
        course = super().create(validated_data)
        QuizBox.objects.create(course=course, owner=course.teacher)
        return course

class CourseDetailSerializer(serializers.ModelSerializer):
    teacher = UserProfileSerializer(read_only=True)
    students = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'course_name', 'teacher', 'students', 'uuid')
        read_only_fields = ('id', 'teacher', 'uuid')


class CourseDefault:
    def set_context(self, serializer_field):
        self.course = Course.objects.get(pk=serializer_field.context['course_id'])

    def __call__(self):
        return self.course


class ArticleSerializer(serializers.ModelSerializer):
    course = serializers.HiddenField(default=CourseDefault())
    _author = serializers.HiddenField(default=serializers.CurrentUserDefault(), source='author')
    author = serializers.StringRelatedField()

    class Meta:
        model = ArticleModel
        fields = ('id', 'title', 'created_at', 'content', 'type', 'course', 'author', '_author', 'file', 'important',)


class NoticeSerializer(ArticleSerializer):
    type = serializers.HiddenField(default=IS_NOTICE)


class TeacherNoticeSerializer(NoticeSerializer):
    class Meta:
        model = ArticleModel
        fields = ('id', 'title', 'created_at', 'content', 'type', 'course', 'author', '_author', 'file', 'important', )


class ReferenceSerializer(ArticleSerializer):
    type = serializers.HiddenField(default=IS_REFERENCE)


class QnASerializer(ArticleSerializer):
    type = serializers.HiddenField(default=IS_QNA)


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    course = serializers.SlugRelatedField(slug_field='course_name', read_only=True)
    course_id = serializers.SlugRelatedField(source='course', slug_field='id', read_only=True)

    class Meta:
        model = ArticleModel
        fields = ('id', 'title', 'created_at', 'author', 'content', 'file', 'type', 'course', 'course_id')
        read_only_fields = ('type', )


class TeacherArticleDetailSerializer(ArticleDetailSerializer):
    class Meta:
        model = ArticleModel
        fields = ('id', 'title', 'created_at', 'author', 'content', 'file', 'type', 'important',)
        read_only_fields = ('type', )

class CommentDefault:
    def set_context(self, serializer_field):
        self.article = ArticleModel.objects.get(pk=serializer_field.context['article_id'])

    def __call__(self):
        return self.article


class CommentSerializer(serializers.ModelSerializer):
    article = serializers.HiddenField(default=CommentDefault())
    _author = serializers.HiddenField(default=serializers.CurrentUserDefault(), source='author')
    author = serializers.StringRelatedField()

    class Meta:
        model = CommentModel
        fields = '__all__'
        extra_fields = ['_author']


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentModel
        fields = ('id', 'author', 'created_at', 'content', )
        read_only_fields = ('id', 'author',)


class CourseApplySerializer(serializers.ModelSerializer):
    apply = serializers.HiddenField(default=serializers.CurrentUserDefault())
    uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = Course
        fields = ('apply', 'uuid', )

    def update(self, instance, validated_data):
        apply = validated_data.pop('apply')
        instance.students.add(apply)
        for quiz in instance.quizbox.quiz.all():
            now = timezone.localtime()
            if now < quiz.due:
                Grade.objects.create(quiz=quiz, gradebox=apply.gradebox)
                print(quiz.due)
        return super().update(instance, validated_data)


class CourseApplySerializer2(CourseApplySerializer):
    def validate(self, attrs):
        _uuid = attrs['_uuid']
        self.instance = Course.objects.get(uuid=_uuid)
        return super().validate(attrs)


class RecentArticleSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    course = serializers.SlugRelatedField(slug_field='course_name', read_only=True)
    course_id = serializers.SlugRelatedField(source='course', slug_field='id', read_only=True)

    class Meta:
        model = ArticleModel
        exclude = ('type', )
