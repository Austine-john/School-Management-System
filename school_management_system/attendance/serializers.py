from rest_framework import serializers

from .models import Attendance


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'date', 'status', 'note', 'recorded_by', 'school',
        ]
        read_only_fields = ['school', 'recorded_by']
