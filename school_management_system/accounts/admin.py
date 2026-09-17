from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.admin import TenantAdmin
from .models import (
    Guardian,
    StaffProfile,
    StudentGuardian,
    StudentProfile,
    TeacherProfile,
)

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = [
        'email', 'first_name', 'last_name', 'role', 'school',
        'is_active', 'is_staff',
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'school']
    search_fields = ['email', 'first_name', 'last_name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role', 'school')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'role', 'school',
                'password1', 'password2',
            ),
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(TenantAdmin):
    list_display = ['student_number', 'user', 'school', 'gender', 'admission_date']
    search_fields = ['student_number', 'user__email', 'user__first_name', 'user__last_name']
    list_filter = ['gender']
    raw_id_fields = ['user']


@admin.register(TeacherProfile)
class TeacherProfileAdmin(TenantAdmin):
    list_display = ['employee_number', 'user', 'school', 'hire_date']
    search_fields = ['employee_number', 'user__email', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']


@admin.register(StaffProfile)
class StaffProfileAdmin(TenantAdmin):
    list_display = ['employee_number', 'user', 'position', 'school']
    search_fields = ['employee_number', 'user__email', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user']


@admin.register(Guardian)
class GuardianAdmin(TenantAdmin):
    list_display = ['user', 'phone', 'school']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'phone']
    raw_id_fields = ['user']


@admin.register(StudentGuardian)
class StudentGuardianAdmin(TenantAdmin):
    list_display = ['student', 'guardian', 'relationship', 'is_primary', 'school']
    list_filter = ['relationship', 'is_primary']
    raw_id_fields = ['student', 'guardian']
