from rest_framework import serializers
from . import models


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Message
        fields = ('id', 'title', 'sender', 'sent_at', 'receiver', 'is_read')

