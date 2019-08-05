import uuid
from django.db import models
from django.conf import settings
from datetime import datetime

# Create your models here.
# from backend.team3.team3.settings import settings.AUTH_USER_MODEL

IS_NOTICE = 0
IS_REFERENCE = 1
IS_QNA = 2

CHOICES = (
    (IS_NOTICE, 'notice'),
    (IS_REFERENCE, 'reference'),
    (IS_QNA, 'qna')
)
# class BoardType(models.Model):
#     IS_NOTICE = 0
#     IS_REFERENCE = 1
#     IS_QNA = 2
#
#     CHOICES = (
#         IS_NOTICE,
#         IS_REFERENCE,
#         IS_QNA
#     )


class Course(models.Model):
    course_name = models.CharField(max_length=20)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_course')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='students_course', blank=True)

    def __str__(self):
        return self.course_name


def upload_to(instance, filename):
    print(instance, filename)
    return 'article/{username}/{year}/{filename}'.format(username=instance.author.username,year=datetime.now().year, filename=filename)

class ArticleModel(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=CHOICES)
    important = models.BooleanField(default=False)
    file = models.FileField(null=True, blank=True, upload_to=upload_to)


class CommentModel(models.Model):
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
