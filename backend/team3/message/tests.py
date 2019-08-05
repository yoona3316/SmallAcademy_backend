from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from message.models import MessageBox, Message


class MessageTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('test', 'test', '12apwgj', 'test@test.com', is_teacher=True)
        MessageBox.objects.create(owner=self.user1)
        self.user2 = User.objects.create_user('test2', 'test2', '12apwgj', 'test2@test.com', is_teacher=True)
        MessageBox.objects.create(owner=self.user2)

    def test_create_message(self):
        url = reverse('send_message')

        data = {"title": "title", "content": "content", "receiver": "test2"}
        resp = self.client.post(url, data)

        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.post(url, data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.user1.message_box.get_sent_message().exists())
        self.assertTrue(self.user2.message_box.get_received_message().exists())

    def test_retrieve_message_box(self):
        url = reverse('message_box')

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        message = Message.objects.create(sender='test2', receiver='test', content='e', title='e')
        message.message_box.add(self.user1.message_box)
        message.message_box.add(self.user2.message_box)

        url = reverse('sent_message_box')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        url = reverse('received_message_box')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data['messages']), 1)

    def test_retrieve_message(self):
        message = Message.objects.create(sender='te', receiver='test', content='e', title='e')
        message.message_box.add(self.user1.message_box)
        url = reverse('get_message', args=[message.id,])

        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        self.client.force_login(self.user2)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_message(self):
        message = Message.objects.create(sender='test2', receiver='test', content='e', title='e')
        message.message_box.add(self.user1.message_box)
        message.message_box.add(self.user2.message_box)
        url = reverse('delete_message', args=[message.id])

        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_login(self.user1)
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.user1.message_box.messages.filter(id=message.id).exists())

    def test_get_unread_num(self):
        url = reverse('unread_num', args=[self.user1.id])

        self.client.force_login(self.user1)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
