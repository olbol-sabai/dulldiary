from rest_framework import permissions

class AnonPermission(permissions.BasePermission):
    message = 'You cannot be logged in for this'

    def has_permission(self, request, view):
        return not request.user.is_authenticated

