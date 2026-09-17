from django.db import models


class School(models.Model):
    """A tenant on the platform. Every tenant-scoped record belongs to a School."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100, unique=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'schools'

    def __str__(self):
        return self.name


class TenantQuerySet(models.QuerySet):
    """QuerySet helper for tenant-scoped models."""

    def for_school(self, school):
        return self.filter(school=school)


class TenantManager(models.Manager.from_queryset(TenantQuerySet)):
    """Manager exposing ``for_school()``. No implicit scoping (scoping is explicit)."""


class TenantModel(models.Model):
    """Abstract base for every model that belongs to a single school.

    Subclasses automatically get a ``school`` foreign key and a
    ``TenantManager``. Data isolation is enforced at the view/query level
    (see ``core.viewsets.TenantModelViewSet``).
    """

    school = models.ForeignKey(
        'core.School',
        on_delete=models.CASCADE,
        related_name='+',
    )

    objects = TenantManager()

    class Meta:
        abstract = True
