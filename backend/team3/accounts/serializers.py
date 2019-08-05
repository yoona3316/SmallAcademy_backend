import re
import socket

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
from .tokens import account_activation_token

from courses.serializers import CourseSerializer
from message.models import MessageBox
from quiz.models import GradeBox

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'realname', 'password', 'email', 'is_teacher', 'profile')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        message_box = MessageBox.objects.create(owner=user)
        GradeBox.objects.create(user=user)
        user.save()

        print(type(force_bytes(user.pk).decode('utf-8')))
        message = render_to_string('account_activate_email.html', {
            'user': user,
            'domain': 'localhost:8000',
            # 'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'uid': user.pk,
            'token': account_activation_token.make_token(user)
        })
        mail_subject = 'test'

        email = EmailMessage(mail_subject, message, to=[user.email])
        email.content_subtype = "html"
        email.send()
        print('email_sent')
        return user

    # password는 영어, 숫자, 특수기호를 조합한 8글자 이상이어야 함
    def validate_password(self, password):
        msg = 'password는 영어, 숫자, 특수기호를 조합한 8글자 이상이어야 합니다.'
        pattern = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if re.match(pattern, password) is None:
            raise ValidationError(msg)
        if len(password)<8:
            raise ValidationError(msg)
        return password


class UserInfoSerializer(serializers.ModelSerializer):
    teacher_course = CourseSerializer(many=True, read_only=True)
    students_course = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'realname', 'email', 'is_teacher', 'profile', 'teacher_course', 'students_course',)
        read_only_fields = ('username', 'realname', 'email', 'is_teacher', 'teacher_course', 'students_course', )

