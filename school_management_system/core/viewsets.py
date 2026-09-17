from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from .tenancy import resolve_school


class TenantModelViewSet(viewsets.ModelViewSet):
    """Base viewset that scopes every query to the request's school.

    - ``get_queryset`` filters by the resolved school when one exists.
    - ``perform_create`` stamps the resolved school onto new objects, refusing
      to create a tenant-scoped record without an explicit school context.
    """

    @property
    def current_school(self):
        if not hasattr(self, '_current_school'):
            self._current_school = resolve_school(self.request)
        return self._current_school

    def get_queryset(self):
        qs = super().get_queryset()
        school = self.current_school
        if school is not None:
            qs = qs.filter(school=school)
        return qs

    def perform_create(self, serializer):
        school = self.current_school
        if school is None:
            raise ValidationError({
                'school': 'A school context is required. Provide the X-School-ID header.',
            })
        serializer.save(school=school)
