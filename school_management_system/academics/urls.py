from rest_framework.routers import DefaultRouter

from .views import (
    AcademicYearViewSet,
    CourseViewSet,
    EnrollmentViewSet,
    SchoolClassViewSet,
    TeacherAssignmentViewSet,
    TermViewSet,
)

router = DefaultRouter()
router.register('academic-years', AcademicYearViewSet, basename='academic-year')
router.register('terms', TermViewSet, basename='term')
router.register('courses', CourseViewSet, basename='course')
router.register('classes', SchoolClassViewSet, basename='class')
router.register('enrollments', EnrollmentViewSet, basename='enrollment')
router.register('teacher-assignments', TeacherAssignmentViewSet, basename='teacher-assignment')

urlpatterns = router.urls
