from django.conf import settings
from django.db import models

from core.models import TenantModel


class Grade(TenantModel):
    student = models.ForeignKey(
        'accounts.StudentProfile',
        on_delete=models.CASCADE,
        related_name='grades',
    )
    course = models.ForeignKey(
        'academics.Course',
        on_delete=models.CASCADE,
        related_name='grades',
    )
    academic_year = models.ForeignKey(
        'academics.AcademicYear',
        on_delete=models.CASCADE,
        related_name='grades',
    )
    term = models.ForeignKey(
        'academics.Term',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='grades',
    )
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    grade_letter = models.CharField(max_length=5, blank=True)
    comment = models.TextField(blank=True)
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_grades',
    )

    class Meta:
        ordering = ['-academic_year__start_date', 'course__name']
        unique_together = [('student', 'course', 'academic_year', 'term')]

    def __str__(self):
        return f'{self.student} - {self.course} ({self.grade_letter or self.score})'
