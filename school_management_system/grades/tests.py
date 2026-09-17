from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from academics.models import AcademicYear, Course
from accounts.models import Guardian, StudentGuardian, StudentProfile
from core.models import School
from .models import Grade
from .views import GradeViewSet

User = get_user_model()


class GradeAccessTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='Test School', slug='test-school')
        self.year = AcademicYear.objects.create(
            school=self.school, name='2025/2026',
            start_date='2025-09-01', end_date='2026-06-30',
        )
        self.course = Course.objects.create(
            school=self.school, code='MATH', name='Mathematics',
        )

        self.student_user = User.objects.create_user(
            email='student@example.com', password='x12345678',
            role=User.Role.STUDENT, school=self.school,
        )
        self.student = StudentProfile.objects.create(
            school=self.school, user=self.student_user, student_number='S001',
        )

        self.parent_user = User.objects.create_user(
            email='parent@example.com', password='x12345678',
            role=User.Role.PARENT, school=self.school,
        )
        self.guardian = Guardian.objects.create(school=self.school, user=self.parent_user)
        StudentGuardian.objects.create(
            school=self.school, student=self.student, guardian=self.guardian,
            relationship='mother',
        )

        Grade.objects.create(
            school=self.school, student=self.student, course=self.course,
            academic_year=self.year, score=85.50,
        )

        self.factory = APIRequestFactory()

    def test_parent_sees_own_child_grades(self):
        view = GradeViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/grades/')
        force_authenticate(request, user=self.parent_user)
        response = view(request)
        students = {r['student'] for r in response.data['results']}
        self.assertEqual(students, {self.student.id})
