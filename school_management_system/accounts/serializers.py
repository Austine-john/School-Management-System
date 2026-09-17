from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

from .models import (
    Guardian,
    StaffProfile,
    StudentGuardian,
    StudentProfile,
    TeacherProfile,
)

User = get_user_model()


class CustomTokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    """Adds role and school claims to the JWT."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        token['school_id'] = user.school_id
        token['full_name'] = user.get_full_name()
        return token


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    password = serializers.CharField(
        write_only=True,
        required=False,
        min_length=8,
        allow_blank=False,
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name', 'role',
            'school', 'is_active', 'date_joined', 'password',
        ]
        read_only_fields = ['school', 'date_joined']

    def validate_role(self, value):
        request = self.context.get('request')
        user = request.user if request else None
        if user and not (
            user.is_superuser or getattr(user, 'role', None) == User.Role.SUPER_ADMIN
        ):
            if value in (User.Role.SUPER_ADMIN, User.Role.SCHOOL_ADMIN):
                raise serializers.ValidationError(
                    'You do not have permission to assign this role.'
                )
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError(
                {'password': 'This field is required on creation.'}
            )
        role = validated_data.get('role')
        validated_data['is_staff'] = role in (
            User.Role.SUPER_ADMIN,
            User.Role.SCHOOL_ADMIN,
        )
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.is_staff = instance.role in (
            User.Role.SUPER_ADMIN,
            User.Role.SCHOOL_ADMIN,
        )
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'student_number', 'date_of_birth', 'gender',
            'admission_date', 'address', 'school',
        ]
        read_only_fields = ['school']

    def validate_user(self, value):
        if value.role != User.Role.STUDENT:
            raise serializers.ValidationError(
                'The linked user must have the "student" role.'
            )
        return value


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'user', 'employee_number', 'date_of_birth', 'gender',
            'hire_date', 'qualification', 'school',
        ]
        read_only_fields = ['school']

    def validate_user(self, value):
        if value.role != User.Role.TEACHER:
            raise serializers.ValidationError(
                'The linked user must have the "teacher" role.'
            )
        return value


class StaffProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffProfile
        fields = [
            'id', 'user', 'employee_number', 'position', 'hire_date', 'school',
        ]
        read_only_fields = ['school']

    def validate_user(self, value):
        if value.role != User.Role.STAFF:
            raise serializers.ValidationError(
                'The linked user must have the "staff" role.'
            )
        return value


class GuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guardian
        fields = ['id', 'user', 'phone', 'address', 'occupation', 'school']
        read_only_fields = ['school']

    def validate_user(self, value):
        if value.role != User.Role.PARENT:
            raise serializers.ValidationError(
                'The linked user must have the "parent" role.'
            )
        return value


class StudentGuardianSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGuardian
        fields = [
            'id', 'student', 'guardian', 'relationship', 'is_primary', 'school',
        ]
        read_only_fields = ['school']
