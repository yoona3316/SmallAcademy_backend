from django.conf.urls import url
from django.urls import path

from courses.models import ArticleModel

from . import views

urlpatterns = [
    path('', views.CourseList.as_view(), name='course'),
    path('<int:pk>/', views.CourseDetail.as_view(), name='course_detail'),

    path('<int:pk>/article/', views.ArticleList.as_view(), name='article_list'),
    path('<int:pk>/article/notice/', views.NoticeArticle.as_view(), name='notice_article_list'),
    path('<int:pk>/article/reference/', views.ReferenceArticle.as_view(), name='reference_article_list'),
    path('<int:pk>/article/qna/', views.QnAArticle.as_view(), name='qna_article_list'),

    path('article/<int:pk>/', views.ArticleDetail.as_view(), name='article_detail'),

    path('article/<int:article_id>/comment/', views.CommentList.as_view(), name='comment_list'),
    path('article/<int:article_id>/comment/<int:pk>/', views.CommentDetail.as_view(), name='comment_detail'),

    # path('<int:course_id>/apply/', views.CourseApply.as_view(), name='course_apply'),
    path('apply/', views.CourseApply.as_view(), name='course_apply2'),

    path('recent/', views.Recent.as_view(), name='recent', ),

    # pk는 course_id
    path('<int:pk>/article/recent/', views.RecentArticle.as_view(), name='recent_article'),
    path('<int:pk>/article/notice/recent', views.RecentNoticeArticle.as_view(), name='recent_notice_article'),
    path('<int:pk>/article/reference/recent', views.RecentReferenceArticle.as_view(), name='recent_reference_article'),
    path('<int:pk>/article/qna/recent', views.RecentQnAArticle.as_view(), name='recent_qna_article'),

    path('<int:course_id>/article/search/', views.ArticleSearch.as_view(), name='article_search'),
    path('<int:course_id>/article/notice/search/', views.NoticeArticleSearch.as_view(), name='notice_article_search'),
    path('<int:course_id>/article/reference/search/', views.ReferenceArticleSearch.as_view(), name='reference_article_search'),
    path('<int:course_id>/article/qna/search/', views.QnAArticleSearch.as_view(), name='qna_article_search'),

]
