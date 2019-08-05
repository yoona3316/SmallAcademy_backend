from rest_framework import permissions

from .models import MessageBox


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        box = MessageBox.objects.get(owner=request.user)
        return len(box.messages.filter(id=obj.id)) is not 0
