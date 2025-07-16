from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author
        return obj.author == request.user

class IsAdminUserForDangerousMethods(permissions.BasePermission):
    """
    Custom permission to only allow admin users to perform dangerous operations.
    """
    def has_permission(self, request, view):
        if request.method in ['DELETE'] and not request.user.is_staff:
            return False
        return True
