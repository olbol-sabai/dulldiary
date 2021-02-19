from rest_framework import permissions


class OnlyOwnerCanUpdateDelete(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS and request.user != obj.user:
            return False
        return True
        