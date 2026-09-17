from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperAdmin(BasePermission):
    """Allow only platform super admins."""

    message = 'Only platform super admins may perform this action.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser:
            return True
        User = get_user_model()
        return getattr(user, 'role', None) == User.Role.SUPER_ADMIN


class IsSchoolAdmin(BasePermission):
    """Allow platform super admins and school administrators."""

    message = 'Only school administrators may perform this action.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_superuser:
            return True
        User = get_user_model()
        return getattr(user, 'role', None) in (
            User.Role.SUPER_ADMIN,
            User.Role.SCHOOL_ADMIN,
        )


class IsTeacher(BasePermission):
    """Administrators and teachers have write access; other roles are read-only.

    Used for gradebook/attendance endpoints where students and parents need to
    read their own (queryset-filtered) records.
    """

    message = 'Only teachers (or administrators) may perform this action.'

    def has_permission(self, request, view):
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        if user.is_superuser:
            return True
        User = get_user_model()
        return getattr(user, 'role', None) in (
            User.Role.SUPER_ADMIN,
            User.Role.SCHOOL_ADMIN,
            User.Role.TEACHER,
        )
