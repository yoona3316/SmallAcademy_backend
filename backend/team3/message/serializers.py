from rest_framework import serializers

from accounts.models import User
from rest_framework.exceptions import ValidationError

from . import models
from . import nest_serializers as nests


class MessageBoxDefault(object):
    def set_context(self, serializer_field):
        user = serializer_field.context['request'].user
        self.message_box = [user.message_box, ]

    def __call__(self):
        return self.message_box


class SendMessageSerializer(serializers.ModelSerializer):
    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    message_box = serializers.HiddenField(default=MessageBoxDefault())

    class Meta:
        model = models.Message
        exclude = ('is_read',)

    def create(self, validated_data):
        str_receiver = validated_data.get('receiver')
        receiver = self.get_user_object(str_receiver)
        return self.send_message(validated_data, receiver)

    def get_user_object(self, receiver):
        try:
            user = User.objects.get(username=receiver)
        except User.DoesNotExist:
            raise ValidationError("아이디가 존재하지 않습니다.")
        return user

    def send_message(self, validated_data, receiver):
        message = super().create(validated_data)
        message.message_box.add(receiver.message_box)
        return message


class MessageBoxSerializer(serializers.ModelSerializer):
    messages = nests.MessageSerializer(many=True)
    owner = serializers.StringRelatedField()

    class Meta:
        model = models.MessageBox
        fields = ('id', 'owner', 'messages', )


class SentMessageBoxSerializer(MessageBoxSerializer):
    messages = nests.MessageSerializer(many=True, source='get_sent_message')


class ReceivedMessageBoxSerializer(MessageBoxSerializer):
    messages = nests.MessageSerializer(many=True, source='get_received_message')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'


class DeleteMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'
