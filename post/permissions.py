from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if hasattr(obj, "posted_by"):
            return obj.posted_by == request.user.profile
        if hasattr(obj, "commented_by"):
            return obj.commented_by == request.user.profile
        if hasattr(obj, "replied_by"):
            return obj.replied_by == request.user.profile
        return False
        