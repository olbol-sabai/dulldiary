from rest_framework import permissions


class MustBeUserOrSafeMethod(permissions.BasePermission):
    message = 'Only users can change user details'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user == obj:
            return True
        return False 