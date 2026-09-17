from rest_framework import serializers

from .models import (
    AcademicYear,
    Course,
    Enrollment,
    SchoolClass,
    TeacherAssignment,
    Term,
)


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'name', 'start_date', 'end_date', 'is_current', 'school']
        read_only_fields = ['school']


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = [
            'id', 'academic_year', 'name', 'start_date', 'end_date',
            'order', 'school',
        ]
        read_only_fields = ['school']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'description', 'school']
        read_only_fields = ['school']


class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = [
            'id', 'name', 'academic_year', 'class_teacher', 'capacity', 'school',
        ]
        read_only_fields = ['school']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            'id', 'student', 'school_class', 'enrollment_date', 'status', 'school',
        ]
        read_only_fields = ['school', 'enrollment_date']


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAssignment
        fields = ['id', 'teacher', 'school_class', 'course', 'school']
        read_only_fields = ['school']
