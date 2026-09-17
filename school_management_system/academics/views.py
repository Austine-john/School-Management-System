from core.permissions import IsSchoolAdmin
from core.viewsets import TenantModelViewSet
from .models import (
    AcademicYear,
    Course,
    Enrollment,
    SchoolClass,
    TeacherAssignment,
    Term,
)
from .serializers import (
    AcademicYearSerializer,
    CourseSerializer,
    EnrollmentSerializer,
    SchoolClassSerializer,
    TeacherAssignmentSerializer,
    TermSerializer,
)


class AcademicYearViewSet(TenantModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsSchoolAdmin]
    filterset_fields = ['is_current']
    search_fields = ['name']
    ordering_fields = ['start_date', 'name']


class TermViewSet(TenantModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    permission_classes = [IsSchoolAdmin]
    filterset_fields = ['academic_year']
    search_fields = ['name']
    ordering_fields = ['order', 'start_date']


class CourseViewSet(TenantModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsSchoolAdmin]
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code']


class SchoolClassViewSet(TenantModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer
    permission_classes = [IsSchoolAdmin]
    filterset_fields = ['academic_year', 'class_teacher']
    search_fields = ['name']
    ordering_fields = ['name']


class EnrollmentViewSet(TenantModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsSchoolAdmin]
    filterset_fields = ['status', 'school_class', 'student']
    ordering_fields = ['enrollment_date']


class TeacherAssignmentViewSet(TenantModelViewSet):
    queryset = TeacherAssignment.objects.all()
    serializer_class = TeacherAssignmentSerializer
    permission_classes = [IsSchoolAdmin]
    filterset_fields = ['teacher', 'school_class', 'course']
