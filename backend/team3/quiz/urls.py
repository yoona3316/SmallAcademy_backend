from django.urls import path

from . import views

urlpatterns = [
    # get, create, update quiz, question
    path('box/all/<int:box_id>/', views.QuizBox.as_view(), name='box'),
    path('quiz/all/<int:box_id>/', views.Quiz.as_view(), name='quiz'),
    path('quiz/detail/<int:quiz_id>/', views.QuizDetail.as_view(), name='quiz_detail'),
    path('question/all/<int:quiz_id>/', views.Question.as_view(), name='question'),
    path('questionall/<int:quiz_id>/', views.QuestionAll.as_view(), name='question_all'),
    path('question/detail/<int:question_id>/', views.QuestionDetail.as_view(), name='question_detail'),
    # answer 추가/삭제하기
    path('answer/append/<int:question_id>/', views.AnswerAppend.as_view(), name='answer_append'),
    path('answer/delete/<int:answer_id>/', views.AnswerDelete.as_view(), name='answer_delete'),
    # 점수 보기
    path('grade/all/<int:quiz_id>/', views.AllStudentsGrade.as_view(), name='all_student_grade'),
    path('grade/box/', views.MyGradeBox.as_view(), name='my_grade_box'),
    path('grade/quiz/<int:course_id>/', views.MyQuizGradeBox.as_view(), name='my_quiz_grade_box'),
    # 채점
    path('grade/question/<int:question_id>/', views.GradeQuestion.as_view(), name='grade_question'),
    path('grade/<int:quiz_id>/', views.GradeQuiz.as_view(), name='grade_quiz'),
    # 곧 마감인 퀴즈 리스트
    path('upcoming/<int:course_id>/', views.UpcomingQuiz.as_view(), name='upcoming_quiz'),
    path('upcoming/', views.UpcomingQuizAll.as_view(), name='upcoming_quiz_all'),
]
