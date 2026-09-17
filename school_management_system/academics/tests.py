from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from core.models import School
from .models import Course
from .views import CourseViewSet

User = get_user_model()


class TenantIsolationTests(TestCase):
    def setUp(self):
        self.school_a = School.objects.create(name='School A', slug='school-a')
        self.school_b = School.objects.create(name='School B', slug='school-b')

        self.admin_a = User.objects.create_user(
            email='admin@a.example.com', password='x12345678',
            role=User.Role.SCHOOL_ADMIN, school=self.school_a,
        )
        self.admin_b = User.objects.create_user(
            email='admin@b.example.com', password='x12345678',
            role=User.Role.SCHOOL_ADMIN, school=self.school_b,
        )

        self.course_a = Course.objects.create(school=self.school_a, code='MATH', name='Math')
        self.course_b = Course.objects.create(school=self.school_b, code='MATH', name='Math')

        self.factory = APIRequestFactory()

    def test_school_admin_only_sees_own_school_courses(self):
        view = CourseViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/courses/')
        force_authenticate(request, user=self.admin_a)
        response = view(request)
        ids = {item['id'] for item in response.data['results']}
        self.assertIn(self.course_a.id, ids)
        self.assertNotIn(self.course_b.id, ids)

    def test_create_stamps_request_school(self):
        view = CourseViewSet.as_view({'post': 'create'})
        request = self.factory.post(
            '/api/v1/courses/', {'code': 'ENG', 'name': 'English'}, format='json',
        )
        force_authenticate(request, user=self.admin_a)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        created = Course.objects.get(code='ENG')
        self.assertEqual(created.school, self.school_a)
