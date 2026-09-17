from django.db import models

from core.models import TenantModel


class AcademicYear(TenantModel):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.name


class Term(TenantModel):
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, related_name='terms',
    )
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    order = models.PositiveSmallIntegerField(default=1)

    class Meta:
        ordering = ['academic_year', 'order']

    def __str__(self):
        return f'{self.academic_year} - {self.name}'


class Course(TenantModel):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        unique_together = [('school', 'code')]

    def __str__(self):
        return f'{self.name} ({self.code})'


class SchoolClass(TenantModel):
    name = models.CharField(max_length=100)
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, related_name='classes',
    )
    class_teacher = models.ForeignKey(
        'accounts.TeacherProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classes',
    )
    capacity = models.PositiveIntegerField(default=30)

    class Meta:
        ordering = ['name']
        verbose_name = 'class'
        verbose_name_plural = 'classes'

    def __str__(self):
        return self.name


class Enrollment(TenantModel):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        WITHDRAWN = 'withdrawn', 'Withdrawn'
        GRADUATED = 'graduated', 'Graduated'
        TRANSFERRED = 'transferred', 'Transferred'

    student = models.ForeignKey(
        'accounts.StudentProfile',
        on_delete=models.CASCADE,
        related_name='enrollments',
    )
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name='enrollments',
    )
    enrollment_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE,
    )

    class Meta:
        ordering = ['school_class', 'student']
        unique_together = [('student', 'school_class')]

    def __str__(self):
        return f'{self.student} -> {self.school_class}'


class TeacherAssignment(TenantModel):
    teacher = models.ForeignKey(
        'accounts.TeacherProfile',
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, related_name='assignments',
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='assignments',
    )

    class Meta:
        ordering = ['school_class', 'course']
        unique_together = [('teacher', 'school_class', 'course')]

    def __str__(self):
        return f'{self.teacher} - {self.course} ({self.school_class})'
