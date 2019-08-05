from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from courses.models import Course
from . import models
# Create your tests here.


class QuizTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('test', 'test', '12apwgj', 'test@test.com', is_teacher=True)
        self.user2 = User.objects.create_user('test2', 'test2', '12apwgj', 'test2@test.com', is_teacher=True)
        self.course = Course.objects.create(course_name='course1', teacher=self.user1)
        self.quiz_box = models.QuizBox.objects.create(course=self.course, owner=self.user1)

    def test_create_quiz(self):
        url = reverse('quiz', args=[self.quiz_box.id])
        data = {
        "title": "퀴즈",
        "due": "2020-01-01T01:00:00Z"
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        self.client.force_login(self.user2)
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


    def test_retrieve_quiz_list(self):
        url = reverse('box', args=[self.quiz_box.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.client.force_login(self.user2)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_quiz_detail(self):
        quiz = models.Quiz.objects.create(title='퀴즈', due='2020-01-01T01:00:00Z', quizbox=self.quiz_box)
        url = reverse('quiz_detail', args=[quiz.id])

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.client.force_login(self.user2)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    # Not working, dont know why...
    def test_update_quiz(self):
        data = {
            "title": "test!!",
            "due": "2020-01-01T01:00:00+09:00"
        }
        quiz = models.Quiz.objects.create(title="퀴즈", due="2020-01-01T01:00:00Z", quizbox=self.quiz_box)
        url = reverse('quiz_detail', args=[quiz.id])
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.client.force_login(self.user2)
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_quiz(self):
        quiz = models.Quiz.objects.create(title='퀴즈', due='2020-01-01T10:00:00+09:00', quizbox=self.quiz_box)
        url = reverse('quiz_detail', args=[quiz.id])

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user2)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

class QuestionTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('test', 'test', '12apwgj', 'test@test.com', is_teacher=True)
        self.user2 = User.objects.create_user('test2', 'test2', '12apwgj', 'test2@test.com', is_teacher=True)
        self.course = Course.objects.create(course_name='course1', teacher=self.user1)
        self.quiz_box = models.QuizBox.objects.create(course=self.course, owner=self.user1)
        self.quiz = models.Quiz.objects.create(title='testquiz', due='2020-01-01T10:00:00+09:00', quizbox=self.quiz_box)
        self.quiz2 = models.Quiz.objects.create(title='testquiz', due='2019-01-01T10:00:00+09:00', quizbox=self.quiz_box)

    def test_create_question(self):
        url = reverse('question', args=[self.quiz.id])
        data = {
            "question": "questiontest!",
            "explanation": "this is explanation",
            "answers": [
                {
                    "answer": "answer1",
                    "is_answer": "false"
                },
                {
                    "answer": "answer2",
                    "is_answer": "false"
                }
            ]
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user2)
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_question_list(self):
        url = reverse('question', args=[self.quiz.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.client.force_login(self.user2)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_question(self):
        question = models.Question.objects.create(question='title', quiz=self.quiz)
        url = reverse('question_detail', args=[question.id])

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_question(self):
        question = models.Question.objects.create(question="question", quiz=self.quiz)
        answer = models.Answer.objects.create(answer="num1", is_answer=False, question=question)
        url = reverse('question_detail', args=[question.id])
        data = {
            "question": "questiontest",
            "explanation": "this is explanation",
            "answers": [
                {
                    id: answer.id,
                    "answer": "answer1",
                    "is_answer": "false"
                }
            ]
        }
        self.client.force_login(self.user2)
        resp = self.client.put(url, data)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_question(self):
        question = models.Question.objects.create(question="question", quiz = self.quiz)
        url = reverse('question_detail', args=[question.id])

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user2)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)







class GradeTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('test', 'test', '12apwgj', 'test@test.com', is_teacher=True)
        self.user2 = User.objects.create_user('test2', 'test2', '12apwgj', 'test2@test.com', is_teacher=True)
        self.gradebox1 = models.GradeBox.objects.create(user=self.user1)
        self.gradebox2 = models.GradeBox.objects.create(user=self.user2)
