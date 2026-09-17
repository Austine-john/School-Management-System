from django.contrib import admin

from core.admin import TenantAdmin
from .models import Grade


@admin.register(Grade)
class GradeAdmin(TenantAdmin):
    list_display = [
        'student', 'course', 'academic_year', 'term', 'score',
        'grade_letter', 'school',
    ]
    list_filter = ['course', 'academic_year', 'term', 'grade_letter']
    search_fields = [
        'student__user__first_name', 'student__user__last_name', 'course__name',
    ]
    raw_id_fields = ['student', 'course', 'academic_year', 'term', 'recorded_by']
