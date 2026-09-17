from rest_framework import viewsets

from .models import School
from .permissions import IsSuperAdmin
from .serializers import SchoolSerializer


class SchoolViewSet(viewsets.ModelViewSet):
    """Platform-level resource managed by super admins only."""

    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsSuperAdmin]
    filterset_fields = ['is_active']
    search_fields = ['name', 'slug', 'email']
    ordering_fields = ['name', 'created_at']
