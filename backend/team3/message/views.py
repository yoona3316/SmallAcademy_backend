from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, Http404
# Create your views here.
from rest_framework import generics, permissions

from accounts.models import User

from . import serializers
from . import models
from .permissions import IsOwner


class SendMessage(generics.CreateAPIView):
    queryset = models.Message.objects.all()
    serializer_class = serializers.SendMessageSerializer
    permission_classes = (permissions.IsAuthenticated, )


class GetMessageBox(generics.RetrieveAPIView):
    queryset = models.MessageBox.objects.all()
    serializer_class = serializers.MessageBoxSerializer

    # 현재 nested serializer로 되어 있어 pagination이 어려우니 nested serializer pagination을 구현할 것
    # https: // stackoverflow.com / questions / 15617595 / paginate - relationship - in -django - rest - framework
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        queryset = self.get_queryset()
        user = self.request.user
        message_box = user.message_box.id
        obj = get_object_or_404(queryset, pk=message_box)
        return obj


class GetSentMessageBox(GetMessageBox):
    serializer_class = serializers.SentMessageBoxSerializer


class GetReceivedMessageBox(GetMessageBox):
    serializer_class = serializers.ReceivedMessageBoxSerializer


class GetMessage(generics.RetrieveAPIView):
    queryset = models.Message.objects.all()
    lookup_url_kwarg = 'message_id'
    lookup_field = 'id'
    serializer_class = serializers.MessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner, )

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user.username != obj.sender:
            obj.is_read = True
        obj.save()
        return super().get(request, *args, **kwargs)


class DeleteMessage(generics.RetrieveDestroyAPIView):
    queryset = models.Message.objects.all()
    serializer_class = serializers.DeleteMessageSerializer
    lookup_url_kwarg = 'message_id'
    lookup_field = 'id'
    permission_classes = (permissions.IsAuthenticated, IsOwner, )

    def perform_destroy(self, instance):
        message_box = models.MessageBox.objects.get(owner=self.request.user)
        message_box.messages.remove(instance)


def GetUnreadMessageNum(request, user_id):
    print(user_id)
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Please Login"})
    if request.method == 'GET':
        box = models.MessageBox.objects.get(owner=user)
        num = 0
        for message in box.messages.all():
            if (not message.is_read) and (message.sender != user.username):
                print(message.sender, user)
                num += 1
        context = {"num": num}
        return JsonResponse(context)
    raise Http404

