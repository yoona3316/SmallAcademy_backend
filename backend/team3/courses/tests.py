import random
import uuid

from django.test import TestCase
# Create your tests here.


class CourseTest(TestCase):
    def setUp(self):
        signupUrl = '/account/signup/'
        res = self.client.post(signupUrl, {'username': 'teacher', 'realname': '선생님', 'email': 'teacher@snu.com', 'password': 'tjstodsla1!', 'is_teacher': True})
        self.assertEqual(res.status_code, 201)
        res = self.client.post(signupUrl, {'username': 'teacher2', 'realname': '선생님2', 'email': 'teacher2@snu.com', 'password': 'tjstodsla2!', 'is_teacher': True})
        self.assertEqual(res.status_code, 201)
        res = self.client.post(signupUrl, {'username': 'student', 'realname': '학생', 'email': 'student@snu.com', 'password': 'gkrtodsla1!'})
        self.assertEqual(res.status_code, 201)
        res = self.client.post(signupUrl, {'username': 'student2', 'realname': '학생2', 'email': 'student2@snu.com', 'password': 'gkrtodsla2!'})
        self.assertEqual(res.status_code, 201)

    def test_login(self):
        loginUrl = '/account/login/'
        res = self.client.post(loginUrl, {'username': 'teacher', 'password': 'tjstodsla1!'})
        self.assertEqual(res.status_code, 200)

    def teacher_login(self, username, password):
        self.client.login(username=username, password=password)

    def student_login(self):
        self.client.login(username='student', password='gkrtodsla1!')

    # CREATE
    def test_post_courselist_teacher(self):
        self.teacher_login('teacher', 'tjstodsla1!')
        postUrl = '/course/'
        res = self.client.post(postUrl, {'course_name': 'test1'})
        self.assertEqual(res.status_code, 201)
        return res

    def test_post_courselist_student(self):
        self.student_login()
        postUrl = '/course/'
        res = self.client.post(postUrl, {'course_name': 'test1'})
        self.assertEqual(res.status_code, 403)

    # RETRIEVE
    def test_get_courselist(self):
        Url = '/course/'
        res = self.client.get(Url)
        self.assertEqual(res.status_code, 200)

    def test_get_course_teacher(self):
        self.test_post_courselist_teacher()
        self.test_login()
        url = '/course/1/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        return res

    # UPDATE
    def test_update_courselist_teacher(self):
        self.test_post_courselist_teacher()
        Url = '/course/1/'
        res = self.client.put(Url, {'course_name': 'updated'},  content_type='application/json',)
        self.assertEqual(res.status_code, 200)

    def test_update_courselist_teacher_noowner(self):
        self.test_post_courselist_teacher()
        Url = '/course/1/'
        self.teacher_login('teacher2', 'tjstodsla2!')
        res = self.client.put(Url, {'course_name': 'updated'},  content_type='application/json',)
        self.assertEqual(res.status_code, 403)

    def test_update_courselist_student(self):
        self.test_post_courselist_teacher()
        Url = '/course/1/'
        self.student_login()
        res = self.client.put(Url, {'course_name': 'updated'}, content_type='application/json',)
        self.assertEqual(res.status_code, 403)

    # DELETE
    def test_delete_courselist_teacher(self):
        # delete course of the owner
        self.test_post_courselist_teacher()
        Url = '/course/1/'
        res = self.client.delete(Url)
        self.assertEqual(res.status_code, 204)

    def test_delete_courselist_teacher_noowner(self):
        self.test_post_courselist_teacher()
        Url = '/course/1/'
        self.teacher_login('teacher2', 'tjstodsla2!')
        res = self.client.delete(Url)
        self.assertEqual(res.status_code, 403)

    def test_delete_courselist_student(self):
        self.test_post_courselist_teacher()
        Url = '/course/1/'
        self.student_login()
        res = self.client.delete(Url)
        self.assertEqual(res.status_code, 403)

    def test_apply_course_right_uuid(self):
        self.test_post_courselist_teacher()
        uuid = self.test_get_course_teacher().data.get('uuid')
        self.student_login()
        url = '/course/apply/'
        res = self.client.put(url, {'uuid': uuid}, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_apply_course_wrong_uuid(self):
        self.test_post_courselist_teacher()
        self.student_login()
        url = '/course/apply/'
        res = self.client.put(url, {'uuid': '12345'}, content_type='application/json')
        self.assertEqual(res.status_code, 404)


class ArticleTest(CourseTest):
    notice = 0
    ref = 1
    qna = 2

    def setUp(self):
        signupUrl = '/account/signup/'
        res = self.client.post(signupUrl, {'username': 'teacher', 'realname': '선생님1', 'email': 'teacher1@snu.com', 'password': 'tjstodsla1!', 'is_teacher': True})
        self.assertEqual(res.status_code, 201)
        res = self.client.post(signupUrl, {'username': 'teacher2', 'realname': '선생님2', 'email': 'teacher2@snu.com', 'password': 'tjstodsla2!', 'is_teacher': True})
        self.assertEqual(res.status_code, 201)
        res = self.client.post(signupUrl, {'username': 'student', 'realname': '학생1', 'email': 'student@snu.com', 'password': 'gkrtodsla1!'})
        self.assertEqual(res.status_code, 201)

    def teacher1_login(self):
        self.client.login(username="teacher", password="tjstodsla1!")

    def teacher2_login(self):
        self.client.login(username="teacher2", password="tjstodsla2!")

    def student1_login(self):
        self.client.login(username="student", password="gkrtodsla1!")

    def student2_login(self):
        self.client.login(username="student2", password="gkrtodsla2!")

    def test_get_aritlce_list_allowed(self):
        course = super().test_post_courselist_teacher()
        self.teacher1_login()
        url = f'/course/{course.data.get("id")}/article/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_article_list_not_allowed(self):
        course = super().test_post_courselist_teacher()
        self.teacher2_login()
        url = f'/course/{course.data.get("id")}/article/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

    def test_get_article_allowed(self):
        article = self.test_post_article_allowed()
        self.teacher1_login()
        url = f'/course/article/{article.data.get("id")}/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_article_not_allowed(self):
        article = self.test_post_article_allowed()
        self.teacher2_login()
        url = f'/course/article/{article.data.get("id")}/'
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

    def test_post_article_allowed(self):
        course = super().test_post_courselist_teacher()
        self.teacher1_login()
        url = f'/course/{course.data.get("id")}/article/'
        res = self.client.post(url, {'title': 'title', 'content': 'content', 'type' :self.notice}, content_type='application/json')
        self.assertEqual(res.status_code, 201)
        return res

    def test_post_article_not_allowed(self):
        course = super().test_post_courselist_teacher()
        self.teacher2_login()
        url = f'/course/{course.data.get("id")}/article/'
        res = self.client.post(url, {'title': 'title', 'content': 'content', 'type' :self.notice}, content_type='application/json')
        self.assertEqual(res.status_code, 403)

    def test_update_article_allowed(self):
        article = self.test_post_article_allowed()
        self.teacher1_login()
        url = f'/course/article/{article.data.get("id")}/'
        res = self.client.put(url, {'title': 'updated', 'content': 'update!'}, content_type='application/json')
        self.assertEqual(res.status_code, 200)

    def test_update_article_not_allowed(self):
        article = self.test_post_article_allowed()
        self.teacher2_login()
        url = f'/course/article/{article.data.get("id")}/'
        res = self.client.put(url, {'title': 'updated', 'content': 'update!'}, content_type='application/json')
        self.assertEqual(res.status_code, 403)

    def test_delete_article_allowed(self):
        article = self.test_post_article_allowed()
        self.teacher1_login()
        url = f'/course/article/{article.data.get("id")}/'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 204)

    def test_delete_article_not_allowed(self):
        article = self.test_post_article_allowed()
        self.teacher2_login()
        url = f'/course/article/{article.data.get("id")}/'
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 403)


class CommentTest(ArticleTest):
    def setUp(self):
        super().setUp()
        self.article = self.test_post_article_allowed()
        self.article_id = self.article.data.get("id")
        self.comment_data = {'content': 'comment test'}
        self.content_type = 'application/json'
        self.url_comment_list = '/course/article/{article_id}/comment/'
        self.url_comment_detail = '/course/article/{article_id}/comment/{comment_id}/'

    def test_get_comment_list_allowed(self):
        self.teacher1_login()
        url = self.url_comment_list.format(article_id=self.article_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
    #
    def test_get_comment_list_not_allowed(self):
        self.teacher2_login()
        url = self.url_comment_list.format(article_id=self.article_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

    def test_get_comment_allowed(self):
        comment_id = self.test_post_comment_allowed().data.get("id")
        self.teacher1_login()
        url = self.url_comment_detail.format(article_id=self.article_id, comment_id=comment_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_get_comment_not_allowed(self):
        comment_id = self.test_post_comment_allowed().data.get("id")
        self.teacher2_login()
        url = self.url_comment_detail.format(article_id=self.article_id, comment_id=comment_id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, 403)

    def test_post_comment_allowed(self):
        self.teacher1_login()
        url = self.url_comment_list.format(article_id=self.article_id)
        res = self.client.post(url, self.comment_data)
        self.assertEqual(res.status_code, 201)
        return res

    def test_post_comment_not_allowed(self):
        self.teacher2_login()
        url = self.url_comment_list.format(article_id=self.article_id)
        res = self.client.post(url, self.comment_data)
        self.assertEqual(res.status_code, 403)

    def test_update_comment_allowed(self):
        comment_id = self.test_post_comment_allowed().data.get("id")
        self.teacher1_login()
        url = self.url_comment_detail.format(article_id=self.article_id, comment_id=comment_id)
        res = self.client.put(url, self.comment_data, content_type=self.content_type)
        self.assertEqual(res.status_code, 200)

    def test_update_comment_not_allowed(self):
        comment_id = self.test_post_comment_allowed().data.get("id")
        self.test_apply_course_right_uuid()
        self.student1_login()
        url = self.url_comment_detail.format(article_id=self.article_id, comment_id=comment_id)
        res = self.client.put(url, self.comment_data, content_type=self.content_type)
        self.assertEqual(res.status_code, 403)
        self.teacher2_login()
        res = self.client.put(url, self.comment_data, content_type=self.content_type)
        self.assertEqual(res.status_code, 403)

    def test_delete_comment_allowed(self):
        comment_id = self.test_post_comment_allowed().data.get("id")
        self.teacher1_login()
        url = self.url_comment_detail.format(article_id=self.article_id, comment_id=comment_id)
        res =self.client.delete(url)
        self.assertEqual(res.status_code, 204)

    def test_delete_comment_not_allowed(self):
        comment_id = self.test_post_comment_allowed().data.get("id")
        self.test_apply_course_right_uuid()
        self.student1_login()
        url = self.url_comment_detail.format(article_id=self.article_id, comment_id=comment_id)
        res =self.client.delete(url)
        self.assertEqual(res.status_code, 403)
        self.teacher2_login()
        res = self.client.delete(url)
        self.assertEqual(res.status_code, 403)
