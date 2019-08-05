from django.contrib import admin
from .models import Course, ArticleModel, CommentModel
# Register your models here.

admin.site.register(Course)
admin.site.register(ArticleModel)
admin.site.register(CommentModel)
