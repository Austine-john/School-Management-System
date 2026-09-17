from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    GuardianViewSet,
    MeView,
    StaffProfileViewSet,
    StudentGuardianViewSet,
    StudentProfileViewSet,
    TeacherProfileViewSet,
    TokenObtainPairView,
    UserViewSet,
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('students', StudentProfileViewSet, basename='student')
router.register('teachers', TeacherProfileViewSet, basename='teacher')
router.register('staff', StaffProfileViewSet, basename='staff')
router.register('guardians', GuardianViewSet, basename='guardian')
router.register('student-guardians', StudentGuardianViewSet, basename='student-guardian')

urlpatterns = [
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MeView.as_view(), name='me'),
]

urlpatterns += router.urls
