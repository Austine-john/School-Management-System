from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView as BaseTokenObtainPairView

from core.permissions import IsSchoolAdmin
from core.tenancy import resolve_school
from core.viewsets import TenantModelViewSet
from .models import (
    Guardian,
    StaffProfile,
    StudentGuardian,
    StudentProfile,
    TeacherProfile,
)
from .serializers import (
    CustomTokenObtainPairSerializer,
    GuardianSerializer,
    StaffProfileSerializer,
    StudentGuardianSerializer,
    StudentProfileSerializer,
    TeacherProfileSerializer,
    UserSerializer,
)

User = get_user_model()


class TokenObtainPairView(BaseTokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.get_full_name(),
            'role': user.role,
            'school_id': user.school_id,
        })


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsSchoolAdmin]
    queryset = User.objects.all()
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['email', 'first_name', 'last_name', 'date_joined']

    def get_queryset(self):
        qs = super().get_queryset()
        school = resolve_school(self.request)
        if school is not None:
            qs = qs.filter(school=school)
        return qs

    def perform_create(self, serializer):
        school = resolve_school(self.request)
        role = serializer.validated_data.get('role')
        if role != User.Role.SUPER_ADMIN and school is None:
            raise ValidationError({
                'school': 'A school context is required for this role. Provide the X-School-ID header.',
            })
        serializer.save(school=school)


class StudentProfileViewSet(TenantModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsSchoolAdmin]
    filterset_fields = ['gender']
    search_fields = [
        'student_number', 'user__first_name', 'user__last_name', 'user__email',
    ]
    ordering_fields = ['student_number', 'user__first_name']


class TeacherProfileViewSet(TenantModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer
    permission_classes = [IsSchoolAdmin]
    search_fields = [
        'employee_number', 'user__first_name', 'user__last_name', 'user__email',
    ]
    ordering_fields = ['employee_number', 'user__first_name']


class StaffProfileViewSet(TenantModelViewSet):
    queryset = StaffProfile.objects.all()
    serializer_class = StaffProfileSerializer
    permission_classes = [IsSchoolAdmin]
    search_fields = [
        'employee_number', 'user__first_name', 'user__last_name', 'user__email',
    ]
    ordering_fields = ['employee_number', 'user__first_name']


class GuardianViewSet(TenantModelViewSet):
    queryset = Guardian.objects.all()
    serializer_class = GuardianSerializer
    permission_classes = [IsSchoolAdmin]
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'phone']
    ordering_fields = ['user__first_name', 'user__last_name']


class StudentGuardianViewSet(TenantModelViewSet):
    queryset = StudentGuardian.objects.all()
    serializer_class = StudentGuardianSerializer
    permission_classes = [IsSchoolAdmin]
    filterset_fields = ['relationship', 'is_primary']
