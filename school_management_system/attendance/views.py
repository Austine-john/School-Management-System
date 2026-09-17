from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from core.permissions import IsTeacher
from core.viewsets import TenantModelViewSet
from .models import Attendance
from .serializers import AttendanceSerializer

User = get_user_model()


class AttendanceViewSet(TenantModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsTeacher]
    filterset_fields = ['student', 'date', 'status']
    ordering_fields = ['date', 'student']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        role = getattr(user, 'role', None)
        if role == User.Role.STUDENT:
            return qs.filter(student__user=user)
        if role == User.Role.PARENT:
            return qs.filter(student__guardians__user=user)
        return qs

    def perform_create(self, serializer):
        school = self.current_school
        if school is None:
            raise ValidationError({
                'school': 'A school context is required. Provide the X-School-ID header.',
            })
        serializer.save(school=school, recorded_by=self.request.user)
