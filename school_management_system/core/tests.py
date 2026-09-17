from django.db import IntegrityError
from django.test import TestCase

from .models import School


class SchoolModelTests(TestCase):
    def test_school_str(self):
        school = School.objects.create(name='Springfield High', slug='springfield-high')
        self.assertEqual(str(school), 'Springfield High')

    def test_school_slug_is_unique(self):
        School.objects.create(name='First', slug='unique-slug')
        with self.assertRaises(IntegrityError):
            School.objects.create(name='Second', slug='unique-slug')
