from django.contrib import admin

from core.admin import TenantAdmin
from .models import (
    AcademicYear,
    Course,
    Enrollment,
    SchoolClass,
    TeacherAssignment,
    Term,
)


@admin.register(AcademicYear)
class AcademicYearAdmin(TenantAdmin):
    list_display = ['name', 'school', 'start_date', 'end_date', 'is_current']
    list_filter = ['is_current']
    search_fields = ['name']


@admin.register(Term)
class TermAdmin(TenantAdmin):
    list_display = ['name', 'academic_year', 'school', 'start_date', 'end_date', 'order']
    list_filter = ['academic_year']
    search_fields = ['name']
    raw_id_fields = ['academic_year']


@admin.register(Course)
class CourseAdmin(TenantAdmin):
    list_display = ['name', 'code', 'school']
    search_fields = ['name', 'code']


@admin.register(SchoolClass)
class SchoolClassAdmin(TenantAdmin):
    list_display = ['name', 'academic_year', 'school', 'class_teacher', 'capacity']
    list_filter = ['academic_year']
    search_fields = ['name']
    raw_id_fields = ['academic_year', 'class_teacher']


@admin.register(Enrollment)
class EnrollmentAdmin(TenantAdmin):
    list_display = ['student', 'school_class', 'status', 'school', 'enrollment_date']
    list_filter = ['status', 'school_class']
    raw_id_fields = ['student', 'school_class']


@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(TenantAdmin):
    list_display = ['teacher', 'course', 'school_class', 'school']
    list_filter = ['course', 'school_class']
    raw_id_fields = ['teacher', 'course', 'school_class']
