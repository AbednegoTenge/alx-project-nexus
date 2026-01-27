from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import (
    LoginSerializer, 
    RegisterSerializer, 
    TokenRefreshResponseSerializer, 
    UserSerializer, 
    ApplyJobSerializer, 
    JobPostingSerializer,
    GetJobSerializer
)
from .services import DashboardService
from .models import JobPosting
from rest_framework.parsers import MultiPartParser, FormParser




class AuthViewSet(GenericViewSet):

    def get_permissions(self):
        if self.action in ['login', 'register']:
            return [AllowAny()]
        return [IsAuthenticated()]

    
    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        elif self.action == 'register':
            return RegisterSerializer
        elif self.action == 'refresh':
            return TokenRefreshResponseSerializer
        return LoginSerializer # Default serializer


    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        access_token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']
        dashboard = DashboardService.get_dashboard(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': access_token,
            'refresh': refresh_token,
            'dashboard': dashboard
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        dashboard = DashboardService.get_dashboard(user)
        return Response({
            'user': UserSerializer(user).data,
            'dashboard': dashboard
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class JobView(ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer

    def get_serializer_class(self):
        if self.action in ['retrieve', 'list', 'get_jobs']:
            return GetJobSerializer
        return JobPostingSerializer

    def get_permissions(self):
        # Public read access, authenticated write access
        if self.action in ['list', 'retrieve', 'get_jobs']:
            return [AllowAny()]
        return [IsAuthenticated()]

    # Override list to show only active jobs
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status=JobPosting.Status.ACTIVE)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Alternative: Keep get_jobs if you want both endpoints
    @action(detail=False, methods=['get'])
    def get_jobs(self, request):
        jobs = JobPosting.objects.filter(status=JobPosting.Status.ACTIVE)
        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='apply', parser_classes=[MultiPartParser, FormParser])
    def apply(self, request, pk=None):
        job = self.get_object()

        serializer = ApplyJobSerializer(
            data=request.data,
            context={
                "request": request,
                "job": job
            }
        )
        serializer.is_valid(raise_exception=True)
        application = serializer.save()

        return Response(
            {
                "message": "Application submitted successfully",
                "application_id": application.id,
                "status": application.status,
            },
            status=status.HTTP_201_CREATED
        )
    
