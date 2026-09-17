from rest_framework import serializers

from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = [
            'id', 'student', 'course', 'academic_year', 'term',
            'score', 'grade_letter', 'comment', 'recorded_by', 'school',
        ]
        read_only_fields = ['school', 'recorded_by']
