from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from accounts.models import StudentProfile
from core.models import School
from .models import Attendance
from .views import AttendanceViewSet

User = get_user_model()


class AttendanceAccessTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Test School', slug='test-school')

        self.student_user = User.objects.create_user(
            email='student@example.com', password='x12345678',
            role=User.Role.STUDENT, school=self.school,
        )
        self.other_student_user = User.objects.create_user(
            email='other@example.com', password='x12345678',
            role=User.Role.STUDENT, school=self.school,
        )
        self.student = StudentProfile.objects.create(
            school=self.school, user=self.student_user, student_number='S001',
        )
        self.other_student = StudentProfile.objects.create(
            school=self.school, user=self.other_student_user, student_number='S002',
        )
        self.teacher = User.objects.create_user(
            email='teacher@example.com', password='x12345678',
            role=User.Role.TEACHER, school=self.school,
        )

        Attendance.objects.create(
            school=self.school, student=self.student, date='2026-01-05',
            status='present',
        )
        Attendance.objects.create(
            school=self.school, student=self.other_student, date='2026-01-05',
            status='absent',
        )

        self.factory = APIRequestFactory()

    def test_student_sees_only_own_attendance(self):
        view = AttendanceViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/attendance/')
        force_authenticate(request, user=self.student_user)
        response = view(request)
        students = {r['student'] for r in response.data['results']}
        self.assertEqual(students, {self.student.id})

    def test_teacher_sees_all_attendance(self):
        view = AttendanceViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/attendance/')
        force_authenticate(request, user=self.teacher)
        response = view(request)
        students = {r['student'] for r in response.data['results']}
        self.assertEqual(students, {self.student.id, self.other_student.id})
