## Quiz API 사용 설명서

quiz/로 접근

### 모델 설명



### api 사용 설명

예) host:port/quiz/box/all/1/

##### QUIZ API - Quiz create, update, delete, get

```python
path('box/all/<int:box_id>/', views.QuizBox.as_view(), name='box')
# box_id의 quizbox를 get하는 api. nested serializer로 quiz를 가지고 있음
# method GET
{
    "id": 2,
    "course_id": 2,
    "course": "science",
    "quiz": [
        {
            "id": 60,
            "title": "test",
            "due": "2019-01-01T01:00:00Z"
        },
        {
            "id": 61,
            "title": "만든다 퀴즈",
            "due": "2019-01-01T01:00:00Z"
        }
    ]
}

path('quiz/all/<int:box_id>/', views.Quiz.as_view(), name='quiz')
# box_id의 quizbox를 외부키로 갖고 있는 quiz들의 리스트를 전부 가지고 오거나 새로운 quiz를 만들 수 있는 api
# method: GET POST
POST 형식
 {
        "title": "퀴즈",
            "due": "2019-01-01T01:00:00Z"
  }
GET return 형식
[
    {
        "id": 60,
        "title": "test",
        "due": "2019-01-01T01:00:00Z"
    },
    {
        "id": 61,
        "title": "만든다 퀴즈",
        "due": "2019-01-01T01:00:00Z"
    }
]

path('quiz/detail/<int:quiz_id>/', views.QuizDetail.as_view(), name='quiz_detail')
# quiz_id 의 quiz를 get, update, delete 할 수 있는 api
# method: GET, PUT, PATCH, DELETE..
PUT, PATCH 형식
{
    "title": "quiztest",
    "due": "2019-01-01T01:00:00Z"
 }
GET return 형식
{
    "id": 1,
    "title": "quiztest",
    "due": "2019-01-01T01:00:00Z"
}

path('question/all/<int:quiz_id>/', views.Question.as_view(), name='question')
# quiz_id의 quiz를 외부키로 갖는 question-answers를 get, create할 수 있는 api
# method: GET, POST
POST 형식
 {
        "question": "questiontest!",
        "explanation": "this is explanation",
        "answers": [
            {
                "answer": "answer1",
                "is_answer": false
            },
            {
                "answer": "answer2",
                "is_answer": true
            }
        ]
 }
GET 형식
[
    {
        "id": 1,
        "question": "this is test question1",
        "explanation": null,
        "answers": [
            {
                "id": 1,
                "answer": "1",
                "is_answer": false
            },
            {
                "id": 2,
                "answer": "2",
                "is_answer": false
            },
            {
                "id": 3,
                "answer": "3",
                "is_answer": false
            }
        ]
    },
    {
        "id": 2,
        "question": "questiontest2",
        "explanation": null,
        "answers": [
            {
                "id": 4,
                "answer": "1",
                "is_answer": false
            },
            {
                "id": 5,
                "answer": "2",
                "is_answer": true
            }
        ]
    }
]

path('questionall/<int:quiz_id>/', views.QuestionAll.as_view(), name='question_all'),
# question을 한꺼번에 만드는 api
# method: GET PUT
PUT 형식
{
    "questions": [
        {
            "question": "questiontest!",
            "explanation": "this is explanation",
            "answers": [
                {
                    "answer": "answer1",
                    "is_answer": false
                },
                {
                    "answer": "answer2",
                    "is_answer": true
                }
            ]
        },
        {
            "question": "questiontest!",
            "explanation": "this is explanation",
            "answers": [
                {
                    "answer": "answer1",
                    "is_answer": false
                },
                {
                    "answer": "answer2",
                    "is_answer": true
                }
            ]
        },
        {
            "question": "questiontest!",
            "explanation": "this is explanation",
            "answers": [
                {
                    "answer": "answer1",
                    "is_answer": false
                },
                {
                    "answer": "answer2",
                    "is_answer": true
                }
            ]
        }
    ]
}

GET 형식
{
    "questions": [
        {	
            "id": 1
            "question": "questiontest!",
            "explanation": "this is explanation",
            "answers": [
                {
                    "id": 1
                    "answer": "answer1",
                    "is_answer": false
                },
                {
                    "id": 1
                    "answer": "answer2",
                    "is_answer": true
                }
            ]
        },
        {
            "id": 1
            "question": "questiontest!",
            "explanation": "this is explanation",
            "answers": [
                {
                    "id": 1
                    "answer": "answer1",
                    "is_answer": false
                },
                {
                    "id": 1
                    "answer": "answer2",
                    "is_answer": true
                }
            ]
        },
        {
            "id": 1
            "question": "questiontest!",
            "explanation": "this is explanation",
            "answers": [
                {
                    "id": 1
                    "answer": "answer1",
                    "is_answer": false
                },
                {
                    "id": 1
                    "answer": "answer2",
                    "is_answer": true
                }
            ]
        }
    ]
}

path('question/detail/<int:question_id>/', views.QuestionDetail.as_view(), name='question_detail'),
# question_id의 question을 get, update, delete할 수 있는 api
# method: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
PUT, PATCH 형식
{
    "id": 1,
    "question": "this is test question1",
    "explanation": null,
    "answers": [
        {
            "id": 1,
            "answer": "1",
            "is_answer": false
        },
        {
            "id": 2,
            "answer": "2",
            "is_answer": false
        },
        {
            "id": 3,
            "answer": "3",
            "is_answer": false
        }
    ]
}

path('answer/append/<int:question_id>/', views.AnswerAppend.as_view(), name='answer_append')
# question_id 의 question 아래에 answer를 append하는 api
# method: POST
POST 형식
{
    "answer": "test",
    "is_answer": false
}
RETURN 형식
{
    "id": 28,
    "answer": "test",
    "is_answer": false
}

path('answer/delete/<int:answer_id>/', views.AnswerDelete.as_view(), name='answer_delete')
#answer_id의 answer를 delete하는 api
# method: DELETE


```

##### GRADING API - 성적 보기 및 채점 api

```python
path('grade/all/<int:quiz_id>/', views.AllStudentsGrade.as_view(), name='all_student_grade')
# quiz_id의 quiz에 참여한 모든 학생들의 성적 보기 api
# method: GET
GET return 형식
[
    {
        "id": 1,
        "grade": 0,
        "is_submitted": false,
        "quiz": 1,
        "gradebox": "stu1",
    },
    {
        "id": 2,
        "grade": 0,
        "is_submitted": false,
        "quiz": 1,
        "gradebox": "stu1",
    },
    {
        "id": 5,
        "grade": 5,
        "is_submitted": true,
        "quiz": 1,
        "gradebox": "stu1",
    }
]

path('grade/box/', views.MyGradeBox.as_view(), name='my_grade_box'),
# request.user가 참여한 모든 quiz의 성적 보기 api
# method: GET
GET return 형식
{
     "id": 14,
    "user": 14,
    "grades": [
        {
            "id": 1,
            "grade": 8,
            "is_submitted": true,
            "quiz_id": 1,
            "quiz": "test",
            "gradebox": 14,
            "course_id": 1,
            "course_name": "course1"
        },
        {
            "id": 2,
            "grade": 3,
            "is_submitted": true,
            "quiz_id": 2,
            "quiz": "test2",
            "gradebox": 14,
            "course_id": 1,
            "course_name": "course1"
        }
    ]
}

path('grade/quiz/<int:course_id>/', views.MyQuizGradeBox.as_view(), name='my_quiz_grade_box')
# course_id 의 course에서 생성된 모든 quiz에서 내가 받은 성적 보기 api
# method: GET
GET return 형식
[
    {
        "id": 1,
        "grade": 8,
        "is_submitted": true,
        "quiz_id": 1,
        "quiz": "test",
        "gradebox": 14
    },
    {
        "id": 2,
        "grade": 3,
        "is_submitted": true,
        "quiz_id": 2,
        "quiz": "test2",
        "gradebox": 14
    }
]

path('grade/question/<int:question_id>/', views.GradeQuestion.as_view(), name='grade_question')
# question_id의 question 채점
# method: GET, PUT, PATCH, HEAD, OPTIONS
# PUT request.data의 is_answer가 정답과 다르면 wrong answer msg 출력, 정답이면 정답인 list를 그대로 반환
PUT 형식
{
    "id": 1,
    "question": "this is test question1",
    "answers": [
        {
            "id": 1,
            "answer": "1",
            "is_answer": false
        },
        {
            "id": 2,
            "answer": "2",
            "is_answer": false
        },
        {
            "id": 3,
            "answer": "test",
            "is_answer": false
        }
    ]
}
정답일 경우
{
    "id": 1,
    "question": "this is test question1",
    "answers": [
        {
            "id": 1,
            "answer": "1",
            "is_answer": false
        },
        {
            "id": 2,
            "answer": "2",
            "is_answer": false
        },
        {
            "id": 3,
            "answer": "test",
            "is_answer": false
        }
    ]
}
정답이 아닐 경우
[
    "Wrong answer!"
]

path('grade/<int:quiz_id>/', views.GradeQuiz.as_view(), name='grade_quiz')
# quiz_id의 quiz의 모든 question 을 채점하는 api
# method: GET, PUT, PATCH, HEAD, OPTIONS
PUT 형식
{
    "_quiz": {
        "questions": [
            {
                "id": 25,
                "question": "appendingtest",
                "explanation": "is it appended?",
                "answers": [
                    {
                        "id": 29,
                        "answer": "testtest",
                        "is_answer": false
                    }
                ]
            },
            {
                "id": 1,
                "question": "appendingtest",
                "explanation": "is it appended?",
                "answers": [
                    {
                        "id": 29,
                        "answer": "testtest",
                        "is_answer": false
                    }
                ]
            }
        ]
    }
}
GET 형식
{
    "id": 5,
    "quiz": "quiztest",
    "is_submitted": "True",
    "grade": 0,
    "wrong_answers": [
        {
            "id": 4,
            "question": "questiontest3",
            "explanation": null,
            "answers": [
                {
                    "id": 8,
                    "answer": "1",
                    "is_answer": false
                },
                {
                    "id": 9,
                    "answer": "2",
                    "is_answer": true
                }
            ]
        }
    ]
}

```

##### Upcoming Quiz API

```python
path('upcoming/<int:course_id>/', views.UpcomingQuiz.as_view(), name='upcoming_quiz')
# 마감이 다가오는 퀴즈를 반환, 오늘 < quiz.due 인 것만 반환함
# method: GET
GET 리턴 형식
{
    "count": 97,
    "next": "http://localhost:8000/quiz/upcoming/1/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "quiztest",
            "due": "2019-01-01T10:00:00+09:00"
        },
        {
            "id": 2,
            "title": "quiztest",
            "due": "2019-01-01T10:00:00+09:00"
        }
    ]
}

path('upcoming/', views.UpcomingQuizAll.as_view(), name='upcoming_quiz_all')
# request.user가 등록한 모든 코스의 퀴즈 중 마감이 다가오는 퀴즈(오늘 <quiz.due) 인 것을 반환
# method: GET
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "test",
            "due": "2020-01-01T01:00:00+09:00",
            "course_id": 1,
            "course_name": "course1"
        },
        {
            "id": 2,
            "title": "test2",
            "due": "2020-01-01T01:00:00+09:00",
            "course_id": 1,
            "course_name": "course1"
        }
    ]
}
```

