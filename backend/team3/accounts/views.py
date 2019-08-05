import traceback

from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .tokens import account_activation_token
from .models import User
from .serializers import UserSerializer
# Create your views here.
from rest_framework.generics import ListCreateAPIView, CreateAPIView, RetrieveUpdateAPIView


class UserSignup(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserActivate(APIView):
    permission_classes = (AllowAny, )

    def get(self, request, uidb64, token):
        try:
            # uid = urlsafe_base64_decode(uidb64).decode()
            # user = User.objects.get(pk=uid)
            user = User.objects.get(pk=uidb64)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        try:
            if user is not None and account_activation_token.check_token(user, token):
                user.active = True
                user.save()
                return Response(user.email+' 계정이 활성화되었습니다.',status = status.HTTP_200_OK)
            else:
                return Response('만료된 링크입니다.', status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(traceback.format_exc())
