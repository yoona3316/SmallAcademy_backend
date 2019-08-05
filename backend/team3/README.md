###실행하기 전###  
pip install -r requirements.txt  
//requirements 설치


### API 설명서 ###

REQ: Required, 반드시 써야 하는 필드

DEF: Default 값 표시

**Accounts**

url 시작 주소: account/

ex) localhost:8000/account/signup/

```python
path('signup/', views.UserSignup.as_view(), name='user_signup')
# method: post
# 유저 회원가입 url
	username: REQ
    realname: REQ
    password: REQ
    email: REQ
    is_teacher: DEF=False
    profile: DEF=null

    "username": "t1",
    "realname": "선생1",
    "password": "pbkdf2_sha256$120000$i7nbcH1iH3h4$5SYlTiBKJQcEJLipaR5glrZWgtFC9+ttB0SaF8KdceM=",
    "email": "t1@n.com",
    "is_teacher": true,
    "profile": ""

path('login/', include('rest_auth.urls'))
# method: post
# 유저 로그인 url

	username: REQ
    password: REQ

    "key": "bdbe5538d6719db629848cd0285ed920927f6055"
path('logout/', include('rest_auth.urls'))
# method: post
# 유저 로그아웃

path('user/', include('rest_auth.urls'))
# method: GET, PUT, DELETE
# 유저 정보

	profile:

    "id": 1,
    "username": "yuna",
    "realname": "관리자",
    "email": "yuna@naver.com",
    "is_teacher": true,
    "profile": null,
    "teacher_course": [
        {
            "id": 4,
            "course_name": "test",
            "teacher": "yuna",
            "students": []
        },
        {
            "id": 5,
            "course_name": "테스트",
            "teacher": "yuna",
            "students": []
        }
    ],
    "students_course": []
```

**Courses**

url 시작주소: course/

ex) localhost:8000/course/

```python
path('', views.CourseList.as_view(), name='course')
# method GET-allowany, POST-TeacherOnly
# 수강반 리스트 가져오거나 post
	coursename:

    "id": 1,
    "course_name": "math",
    "teacher": "t1",
    "students": []

path('<int:pk>/', views.CourseDetail.as_view(), name='course_detail')
# method: GET-allowAny, PUT, DELETE-Owner
# 수강반 정보 디테일 가져오거나 수정, 삭제
	coursename:

    "id": 4,
    "course_name": "test",
    "teacher": 1,
    "students": [],
    "uuid": "cb2f987f-0565-43be-bdcb-d872e8206ad2"

path('<int:pk>/article/', views.ArticleList.as_view(), name='article_list')
# method: GET, POST - member of course
# pk 수강반의 게시글 리스트 전체

	title:
    content:
    type: 0 for notice, 1 for reference, 2 for qna
    file: null True

    "id": 1,
    "title": "notice1",
	"created_at": "2019-05-03T07:24:27.956370Z",
    "content": "테스트",
    "type": 0,
    "author": "t1",
    "file":

path('<int:pk>/article/notice/', views.NoticeArticle.as_view(), name='notice_article_list'),
# method: GET, POST - member of course
# pk 수강반의 공지 게시글 리스트

	title:
    content:
    file: null True
    important: default False, permission only to teacher    
        

    "id": 1,
    "title": "notice1",
    "created_at": "2019-05-03T07:24:27.956370Z",
	"content": "테스트",
    "author": "t1",
     "file":

path('<int:pk>/article/reference/', views.ReferenceArticle.as_view(), name='reference_article_list'),
# method: GET, POST - member of course
# pk 수강반의 자료실 게시글 리스트

	title:
    content:
    file: null True

    "id": 1,
    "title": "notice1",
	"created_at": "2019-05-03T07:24:27.956370Z",
    "content": "테스트",
    "author": "t1",
     "file": 

path('<int:pk>/article/qna/', views.QnAArticle.as_view(), name='qna_article_list'),
# method: GET, POST - member of course
# pk 수강반의 질문 게시글 리스트

	title:
    content:
    file: null True

    "id": 1,
    "title": "notice1",
	"created_at": "2019-05-03T07:24:27.956370Z",
    "content": "테스트",
    "author": "t1"
    "file": 

        #여기서부터!!
path('article/<int:pk>/', views.ArticleDetail.as_view(), name='article_detail'),
# method: GET - member of course, PUT, DELETE - owner or readonly
# pk 게시글의 디테일
	title:
    content:
    file: null True
    important: default False, (permitted only for teacher)

    "id": 2,
    "title": "course2ref1",
    "created_at": "2019-05-03T07:17:16.200379Z",
    "author": 2,
    "content": "test",
     "file": 
     "type": 0, 
     "important": false(default=false)

path('article/<int:article_id>/comment/', views.CommentList.as_view(), name='comment_list'),
# method: GET, POST (permission unset yet)
# article_id 번째 게시글의 comment들의 리스트

	content:

	"id": 4,
    "author": "t1",
    "created_at": "2019-05-03T09:13:40.154325Z",
    "content": "course2 comment"

path('article/<int:article_id>/comment/<int:pk>/', views.CommentDetail.as_view(), name='comment_detail'),
# method: GET, PUT, DELETE (permission unset yet)
# pk commnet의 디테일

	content:

	"id": 1,
    "author": 2,
    "created_at": "2019-05-04T04:41:57.707214Z",
    "content": "course1 comment 수정중!!"

path('apply/', views.CourseApply.as_view(), name='course_apply'),
# method: PUT - allowAny
# if key == course.uuid, coruse_id 번째 course에 request.user를 추가

	uuid:

    return nothing


```

    path('<int:course_id>/apply/', views.CourseApply.as_view(), name='course_apply')
    
    #method: PUT - allow Any
    uuid:
    
    return nothing


```
    path('recent/', views.Recent.as_view(), name='recent', ),
    # recent notice articles for request.user
    # method: GET

```
```
   path('<int:pk>/article/recent/', views.RecentArticle.as_view(), name='recent_article_list'),
   # recent article for pk course(including notice, ref, qna)
   
   #method: GET - IsMemberOfCourseOrNotAllowed 
   GET 리턴 형식
   {
            "id": 113,
            "author": "t1",
            "course": "math",
            "course_id": 1,
            "title": "test",
            "created_at": "2019-06-04T16:20:12.380183+09:00",
            "content": "test",
            "important": false,
            "file": "http://localhost:8000/media/article/t1/2019/%EC%86%8C%EA%B0%9C%EC%9B%90%EC%8B%A4%EB%B0%9C%ED%91%9C2.pdf"
   } 
   
```

```
    path('<int:pk>/article/notice/recent', views.RecentNoticeArticle.as_view(), name='recent_notice_article'),
    # recent notice article for pk course
    
    #method: GET - IsMemberOfCourseOrNotAllowed 
    
    path('<int:pk>/article/reference/recent', views.RecentReferenceArticle.as_view(), name='recent_reference_article'),
    # recent ref article for pk course
    
    #method: GET - IsMemberOfCourseOrNotAllowed 
    
    path('<int:pk>/article/qna/recent', views.RecentQnAArticle.as_view(), name='recent_qna_article'),
    #recent qna aritcle for pk course
    
    #method: GET - IsMemberOfCourseOrNotAllowed 
```

```python
path('<int:course_id>/article/search/', views.ArticleSearch.as_view(), name='article_search'),
# search article for course_id course by given kwargs in title, author, content through uri
# usage example
# course/1/article/search/?search=10

path('<int:course_id>/article/notice/search/', views.NoticeArticleSearch.as_view(), name='notice_article_search'),
# search notice article for course_id course by given kwargs in title, author, content through uri
# usage example
# course/1/article/notice/search/?search=10

path('<int:course_id>/article/reference/search/', views.ReferenceArticleSearch.as_view(), name='reference_article_search'),
# search reference article for course_id course by given kwargs in title, author, content through uri
# usage example
# course/1/article/reference/search/?search=10

path('<int:course_id>/article/qna/search/', views.QnAArticleSearch.as_view(), name='qna_article_search'),
# search qna article for course_id course by given kwargs in title, author, content through uri
# usage example
# course/1/article/qna/search/?search=10
```

