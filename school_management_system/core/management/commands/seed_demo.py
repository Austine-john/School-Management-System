from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from academics.models import (
    AcademicYear,
    Course,
    Enrollment,
    SchoolClass,
    TeacherAssignment,
    Term,
)
from accounts.models import (
    Guardian,
    StudentGuardian,
    StudentProfile,
    TeacherProfile,
)
from attendance.models import Attendance
from core.models import School
from grades.models import Grade

User = get_user_model()

PASSWORD = 'demoPass123'


class Command(BaseCommand):
    help = 'Seed a demo school with sample data for local development.'

    def handle(self, *args, **options):
        # Platform owner (super admin)
        super_admin, _ = User.objects.get_or_create(
            email='owner@example.com',
            defaults={'role': User.Role.SUPER_ADMIN},
        )
        super_admin.is_superuser = True
        super_admin.is_staff = True
        super_admin.set_password(PASSWORD)
        super_admin.save()

        # Demo school
        school, _ = School.objects.get_or_create(
            slug='springfield-high',
            defaults={
                'name': 'Springfield High School',
                'address': '123 Main St',
                'email': 'info@springfield-high.example.com',
            },
        )

        # School admin
        school_admin, _ = User.objects.get_or_create(
            email='admin@springfield.example.com',
            defaults={
                'role': User.Role.SCHOOL_ADMIN,
                'school': school,
                'first_name': 'Ada',
                'last_name': 'Admin',
                'is_staff': True,
            },
        )
        school_admin.set_password(PASSWORD)
        school_admin.save()

        # Teacher + profile
        teacher, _ = User.objects.get_or_create(
            email='teacher@springfield.example.com',
            defaults={
                'role': User.Role.TEACHER,
                'school': school,
                'first_name': 'Terry',
                'last_name': 'Teach',
            },
        )
        teacher.set_password(PASSWORD)
        teacher.save()
        teacher_profile, _ = TeacherProfile.objects.get_or_create(
            school=school, user=teacher, defaults={'employee_number': 'T001'},
        )

        # Student + profile
        student, _ = User.objects.get_or_create(
            email='student@springfield.example.com',
            defaults={
                'role': User.Role.STUDENT,
                'school': school,
                'first_name': 'Sam',
                'last_name': 'Student',
            },
        )
        student.set_password(PASSWORD)
        student.save()
        student_profile, _ = StudentProfile.objects.get_or_create(
            school=school, user=student, defaults={'student_number': 'S001'},
        )

        # Parent + guardian + link
        parent, _ = User.objects.get_or_create(
            email='parent@springfield.example.com',
            defaults={
                'role': User.Role.PARENT,
                'school': school,
                'first_name': 'Pat',
                'last_name': 'Parent',
            },
        )
        parent.set_password(PASSWORD)
        parent.save()
        guardian, _ = Guardian.objects.get_or_create(
            school=school, user=parent, defaults={'phone': '555-0100'},
        )
        StudentGuardian.objects.get_or_create(
            school=school, student=student_profile, guardian=guardian,
            defaults={'relationship': StudentGuardian.Relationship.MOTHER},
        )

        # Academic year + term
        year, _ = AcademicYear.objects.get_or_create(
            school=school, name='2025/2026',
            defaults={
                'start_date': '2025-09-01',
                'end_date': '2026-06-30',
                'is_current': True,
            },
        )
        term, _ = Term.objects.get_or_create(
            school=school, academic_year=year, order=1,
            defaults={
                'name': 'First Term',
                'start_date': '2025-09-01',
                'end_date': '2025-12-15',
            },
        )

        # Course
        course, _ = Course.objects.get_or_create(
            school=school, code='MATH', defaults={'name': 'Mathematics'},
        )

        # Class
        klass, _ = SchoolClass.objects.get_or_create(
            school=school, name='Grade 5A',
            defaults={
                'academic_year': year,
                'class_teacher': teacher_profile,
                'capacity': 30,
            },
        )

        # Enrollment
        Enrollment.objects.get_or_create(
            school=school, student=student_profile, school_class=klass,
        )

        # Teacher assignment
        TeacherAssignment.objects.get_or_create(
            school=school, teacher=teacher_profile, school_class=klass, course=course,
        )

        # Attendance
        Attendance.objects.get_or_create(
            school=school, student=student_profile, date='2026-01-05',
            defaults={'status': Attendance.Status.PRESENT, 'recorded_by': teacher},
        )

        # Grade
        Grade.objects.get_or_create(
            school=school, student=student_profile, course=course,
            academic_year=year, term=term,
            defaults={'score': 88.50, 'grade_letter': 'A', 'recorded_by': teacher},
        )

        self.stdout.write(self.style.SUCCESS('Demo data seeded successfully.'))
        self.stdout.write(f'Super admin:  owner@example.com / {PASSWORD}')
        self.stdout.write(f'School admin: admin@springfield.example.com / {PASSWORD}')
