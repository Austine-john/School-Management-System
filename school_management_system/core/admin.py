from django.contrib import admin

from .models import School


class TenantAdmin(admin.ModelAdmin):
    """Admin base that scopes objects to the current user's school.

    Super admins see everything; tenant users only see their own school's rows.
    New objects are automatically stamped with the creating user's school.
    """

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        school = getattr(request.user, 'school', None)
        if school is not None:
            return qs.filter(school=school)
        return qs.none()

    def save_model(self, request, obj, form, change):
        if not change and getattr(obj, 'school_id', None) is None:
            obj.school = getattr(request.user, 'school', None)
        super().save_model(request, obj, form, change)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'slug', 'email')
    prepopulated_fields = {'slug': ('name',)}
