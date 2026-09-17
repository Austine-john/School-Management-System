from django.contrib import admin

from core.admin import TenantAdmin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(TenantAdmin):
    list_display = ['student', 'date', 'status', 'school', 'recorded_by']
    list_filter = ['status', 'date']
    search_fields = ['student__user__first_name', 'student__user__last_name']
    raw_id_fields = ['student', 'recorded_by']
