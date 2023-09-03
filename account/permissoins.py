from rest_framework.permissions import BasePermission


class IsOwnerOfProfile(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.email == obj.email