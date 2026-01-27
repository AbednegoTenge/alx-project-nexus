from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, JobView


# Create a router and register viewsets
router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'jobs', JobView, basename='jobs')

urlpatterns = [
    path('', include(router.urls)),
]
