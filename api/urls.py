from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    login, logout,
    AccountViewSet, LeadViewSet, EmailViewSet,
    MessageTemplateViewSet, SubjectTemplateViewSet
)

router = DefaultRouter()
router.register(r'accounts', AccountViewSet, basename='account')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'emails', EmailViewSet, basename='email')
router.register(r'message-templates', MessageTemplateViewSet, basename='message-template')
router.register(r'subject-templates', SubjectTemplateViewSet, basename='subject-template')

urlpatterns = [
    path('auth/login', login, name='login'),
    path('auth/logout', logout, name='logout'),
    path('', include(router.urls)),
]

