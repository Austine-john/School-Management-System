from django.contrib.auth import get_user_model

from .models import School


def resolve_school(request):
    """Return the School the current request should be scoped to, or ``None``.

    - Tenant users (admin/teacher/staff/student/parent) are always scoped to
      their own ``user.school``.
    - Platform super admins have no inherent school; they can target one
      explicitly via the ``X-School-ID`` header, otherwise they act across
      schools (no scoping).
    """
    user = getattr(request, 'user', None)
    if user is None or not getattr(user, 'is_authenticated', False):
        return None

    User = get_user_model()
    if user.is_superuser or getattr(user, 'role', None) == User.Role.SUPER_ADMIN:
        school_id = request.headers.get('X-School-ID')
        if school_id:
            try:
                return School.objects.get(pk=school_id)
            except (School.DoesNotExist, ValueError, TypeError):
                return None
        return None

    return getattr(user, 'school', None)
