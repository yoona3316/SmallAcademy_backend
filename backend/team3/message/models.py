from django.db import models
from django.conf import settings
# Create your models here.
from django.db import models
from django.conf import settings


class MessageBox(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_box')

    def get_sent_message(self):
        return Message.objects.filter(message_box=self, sender=self.owner)

    def get_received_message(self):
        return Message.objects.filter(message_box=self, receiver=self.owner)

class Message(models.Model):
    message_box = models.ManyToManyField(MessageBox, related_name='messages')
    title = models.CharField(max_length=50, default="(제목없음)")
    sent_at = models.DateTimeField(auto_now=True)
    content = models.TextField(default="(내용없음)")
    sender = models.CharField(max_length=20)
    receiver = models.CharField(max_length=20)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ('-sent_at', )
