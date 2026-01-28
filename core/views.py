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
    GetJobSerializer,
    CandidateProfileSerializer,
    EmployerProfileSerializer
)
from .services import (
    SavedJobsService,
    ApplicationService, 
    NotificationService,
    ReviewService,
)
from .models import JobPosting, CandidateProfile, EmployerProfile
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
        return Response({
            'user': UserSerializer(user).data,
            'access': access_token,
            'refresh': refresh_token,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        return Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user's profile"""
        user = request.user
        
        if user.is_candidate:
            try:
                profile = CandidateProfile.objects.prefetch_related(
                    'candidate_skills__skill',
                    'education',
                    'certifications'
                ).get(user=user)
                serializer = CandidateProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CandidateProfile.DoesNotExist:
                return Response(
                    {'error': 'Candidate profile not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        elif user.is_employer:
            try:
                profile = user.employer_profile
                serializer = EmployerProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except EmployerProfile.DoesNotExist:
                return Response(
                    {'error': 'Employer profile not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(
            {'error': 'User role not recognized'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['patch', 'put'], parser_classes=[MultiPartParser, FormParser])
    def update_profile(self, request):
        """Update current user's profile"""
        user = request.user
        partial = request.method == 'PATCH'
        
        if user.is_candidate:
            try:
                profile = user.candidate_profile
                serializer = CandidateProfileSerializer(
                    instance=profile,
                    data=request.data,
                    partial=partial,
                    context={'request': request}
                )
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            except CandidateProfile.DoesNotExist:
                return Response(
                    {'error': 'Candidate profile not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        elif user.is_employer:
            try:
                profile = user.employer_profile
                serializer = EmployerProfileSerializer(
                    instance=profile,
                    data=request.data,
                    partial=partial,
                    context={'request': request}
                )
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            except EmployerProfile.DoesNotExist:
                return Response(
                    {'error': 'Employer profile not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(
            {'error': 'User role not recognized'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def applications(self, request):
        user = request.user
        if user.is_candidate:
            data = ApplicationService.get_candidate_applications(user)
        elif user.is_employer:
            data = ApplicationService.get_employer_applications(user)
        else:
            data = []
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def notifications(self, request):
        user = request.user
        data = NotificationService.get_notifications(user, limit=None)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def reviews(self, request):
        user = request.user
        data = ReviewService.get_reviews(user, limit=None)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def saved_jobs(self, request):
        user = request.user
        data = SavedJobsService.get_saved_jobs(user, limit=None)
        return Response(data, status=status.HTTP_200_OK)

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
        if self.action in ['retrieve']:
            return GetJobSerializer
        return JobPostingSerializer

    def get_permissions(self):
        # Public read access, authenticated write access
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    # Override list to show only active jobs
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status=JobPosting.Status.ACTIVE)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
        )from rest_framework.viewsets import ModelViewSet, GenericViewSet
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
    GetJobSerializer,
    CandidateProfileSerializer,
    EmployerProfileSerializer
)
from .services import (
    SavedJobsService,
    ApplicationService, 
    NotificationService,
    ReviewService,
)
from .models import JobPosting, CandidateProfile, EmployerProfile
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
        return Response({
            'user': UserSerializer(user).data,
            'access': access_token,
            'refresh': refresh_token,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        return Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def profile(self, request):
        """Get current user's profile"""
        user = request.user
        
        if user.is_candidate:
            try:
                profile = CandidateProfile.objects.prefetch_related(
                    'candidate_skills__skill',
                    'education',
                    'certifications'
                ).get(user=user)
                serializer = CandidateProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except CandidateProfile.DoesNotExist:
                return Response(
                    {'error': 'Candidate profile not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        elif user.is_employer:
            try:
                profile = user.employer_profile
                serializer = EmployerProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except EmployerProfile.DoesNotExist:
                return Response(
                    {'error': 'Employer profile not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(
            {'error': 'User role not recognized'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['patch', 'put'], parser_classes=[MultiPartParser, FormParser])
    def update_profile(self, request):
        """Update current user's profile"""
        user = request.user
        partial = request.method == 'PATCH'
        
        if user.is_candidate:
            try:
                profile = user.candidate_profile
                serializer = CandidateProfileSerializer(
                    instance=profile,
                    data=request.data,
                    partial=partial,
                    context={'request': request}
                )
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            except CandidateProfile.DoesNotExist:
                return Response(
                    {'error': 'Candidate profile not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        elif user.is_employer:
            try:
                profile = user.employer_profile
                serializer = EmployerProfileSerializer(
                    instance=profile,
                    data=request.data,
                    partial=partial,
                    context={'request': request}
                )
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            except EmployerProfile.DoesNotExist:
                return Response(
                    {'error': 'Employer profile not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(
            {'error': 'User role not recognized'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def applications(self, request):
        user = request.user
        if user.is_candidate:
            data = ApplicationService.get_candidate_applications(user)
        elif user.is_employer:
            data = ApplicationService.get_employer_applications(user)
        else:
            data = []
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def notifications(self, request):
        user = request.user
        data = NotificationService.get_notifications(user, limit=None)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def reviews(self, request):
        user = request.user
        data = ReviewService.get_reviews(user, limit=None)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def saved_jobs(self, request):
        user = request.user
        data = SavedJobsService.get_saved_jobs(user, limit=None)
        return Response(data, status=status.HTTP_200_OK)

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
        if self.action in ['retrieve']:
            return GetJobSerializer
        return JobPostingSerializer

    def get_permissions(self):
        # Public read access, authenticated write access
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    # Override list to show only active jobs
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(status=JobPosting.Status.ACTIVE)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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