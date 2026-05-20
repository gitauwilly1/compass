from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrHasRole(BasePermission):
    """Allow read-only to anyone, and write only to the author or privileged roles."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role in ['journalist', 'editor', 'admin', 'superadmin']

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.role in ['editor', 'admin', 'superadmin']:
            return True
        return obj.author == request.user
