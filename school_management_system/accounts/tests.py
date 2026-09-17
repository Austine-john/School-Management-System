from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from core.models import School
from core.tenancy import resolve_school

User = get_user_model()


class UserManagerTests(TestCase):
    def test_create_user_normalizes_email(self):
        user = User.objects.create_user(
            email='Test@Example.com',
            password='supersecret123',
            role=User.Role.TEACHER,
        )
        self.assertEqual(user.email, 'Test@example.com')
        self.assertTrue(user.check_password('supersecret123'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email='admin@example.com',
            password='supersecret123',
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.role, User.Role.SUPER_ADMIN)

    def test_email_is_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='supersecret123')


class ResolveSchoolTests(TestCase):
    def setUp(self):
        self.school = School.objects.create(name='North High', slug='north-high')
        self.factory = APIRequestFactory()

    def _request_for(self, user, headers=None):
        request = self.factory.get('/')
        request.user = user
        request.headers = headers or {}
        return request

    def test_tenant_user_scoped_to_own_school(self):
        user = User.objects.create_user(
            email='admin@north.example.com',
            password='x12345678',
            role=User.Role.SCHOOL_ADMIN,
            school=self.school,
        )
        self.assertEqual(resolve_school(self._request_for(user)), self.school)

    def test_super_admin_not_scoped_by_default(self):
        user = User.objects.create_superuser(
            email='platform@example.com',
            password='x12345678',
        )
        self.assertIsNone(resolve_school(self._request_for(user)))

    def test_super_admin_scoped_via_header(self):
        user = User.objects.create_superuser(
            email='platform@example.com',
            password='x12345678',
        )
        request = self._request_for(user, headers={'X-School-ID': str(self.school.id)})
        self.assertEqual(resolve_school(request), self.school)
