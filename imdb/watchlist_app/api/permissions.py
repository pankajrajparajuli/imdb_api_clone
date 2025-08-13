from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser):
    """
    Custom permission to only allow admin users to edit objects.
    Non-admin users can only read objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    
class ReviewUserorReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the user who created the review to edit it.
    Other users can only read the review.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.review_user == request.user