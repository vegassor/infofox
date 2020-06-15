from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    message = 'Вы должны быть владельцем этого объекта'

    def has_permission(self, request, view, obj):
        return obj.user == request.user

# class IsOwnerOrReadonly(BasePermission):
#     pass
