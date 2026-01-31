from core.models import CompanyReview, Application
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
    EmployerProfileSerializer,
    NotificationSerializer,
    ReviewSerializer,
    ApplicationSerializer
)
from .services import (
    SavedJobsService,
    ApplicationService, 
    NotificationService,
    ReviewService,
)
from .models import JobPosting, CandidateProfile, EmployerProfile, Notification, Application
from rest_framework.parsers import MultiPartParser, FormParser
from .utils import generate_resume_url



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
                profile = user.candidate
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
                profile = user.employer_profile  # Fixed: was user.employer
                serializer = EmployerProfileSerializer(
                    instance=profile,
                    data=request.data,
                    partial=partial,
                    context={'request': request}
                )
                
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)  # Fixed: was 201
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Fixed: Added return
            
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
        """Get user's applications (candidate's or employer's)"""
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
        """Get user's notifications"""
        user = request.user
        data = NotificationService.get_notifications(user, limit=None)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def reviews(self, request):
        """Get user's reviews (employer only)"""
        user = request.user
        if not user.is_employer:
            return Response(
                {'error': 'Only employers can view reviews'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        data = ReviewService.get_reviews(user, limit=None)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def saved_jobs(self, request):
        """Get user's saved jobs (candidate only)"""
        user = request.user
        if not user.is_candidate:
            return Response(
                {'error': 'Only candidates can save jobs'}, 
                status=status.HTTP_403_FORBIDDEN
            )
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

    def get_queryset(self):
        """Filter queryset based on user role"""
        if self.action in ['list']:
            # Public: only show active jobs
            return self.queryset.filter(status=JobPosting.Status.ACTIVE, is_active=True)
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Employer: only their own jobs
            if self.request.user.is_authenticated and self.request.user.is_employer:
                return self.queryset.filter(employer=self.request.user.employer_profile)
        return self.queryset

    def list(self, request, *args, **kwargs):
        """List all active jobs"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """Create a new job posting (employer only)"""
        if not request.user.is_employer:
            return Response(
                {'error': 'Only employers can create job postings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update job posting (employer only, must own the job)"""
        if not request.user.is_employer:
            return Response(
                {'error': 'Only employers can update job postings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        job = self.get_object()
        if job.employer != request.user.employer_profile:
            return Response(
                {'error': 'You can only update your own job postings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Partial update job posting (employer only, must own the job)"""
        if not request.user.is_employer:
            return Response(
                {'error': 'Only employers can update job postings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        job = self.get_object()
        if job.employer != request.user.employer_profile:
            return Response(
                {'error': 'You can only update your own job postings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete job posting (employer only, must own the job)"""
        if not request.user.is_employer:
            return Response(
                {'error': 'Only employers can delete job postings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        job = self.get_object()
        if job.employer != request.user.employer_profile:
            return Response(
                {'error': 'You can only delete your own job postings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='apply', parser_classes=[MultiPartParser, FormParser])
    def apply(self, request, pk=None):
        """Apply for a job (candidate only)"""
        if not request.user.is_candidate:
            return Response(
                {'error': 'Only candidates can apply for jobs'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
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



class ApplicationView(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter applications based on user role"""
        user = self.request.user
        
        if user.is_candidate:
            # Candidates see only their own applications
            return self.queryset.filter(candidate__user=user, is_active=True)
        elif user.is_employer:
            # Employers see applications for their jobs
            return self.queryset.filter(job__employer__user=user, is_active=True)
        
        return self.queryset.none()

    @action(detail=True, methods=['post'], url_path='download-resume')
    def download_resume(self, request, pk=None):
        """Generate signed URL for downloading applicant resume (employer only)"""
        user = request.user
        
        if not user.is_employer:
            return Response(
                {'error': 'Only employers can download resumes'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get the application
        application = self.get_object()
        
        # Verify employer owns the job this application is for
        if application.job.employer.user != user:
            return Response(
                {'error': 'You can only download resumes for your own job postings'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if application has a resume
        if not application.resume:
            return Response(
                {'error': 'This application does not have a resume'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        try:
            # Generate presigned URL for the resume
            resume_url = generate_resume_url(application.resume.name, expires=3600)  # 1 hour expiry
            
            return Response({
                'resume_url': resume_url,
                'applicant_name': application.candidate.user.get_full_name(),
                'expires_in': 3600,  # seconds
                'message': 'Resume URL generated successfully. Link expires in 1 hour.'
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                {'error': f'Failed to generate resume URL: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class NotificationView(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Users can only see their own notifications"""
        return self.queryset.filter(user=self.request.user).order_by('-created_at')

    @action(detail=True, methods=['post'], url_path='mark-read')
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({
            'message': 'Notification marked as read',
            'is_read': notification.is_read
        }, status=status.HTTP_200_OK)



class ReviewView(ModelViewSet):
    queryset = CompanyReview.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter reviews based on user role"""
        user = self.request.user
        
        # Anyone can view all reviews (for browsing companies)
        if self.action in ['list', 'retrieve']:
            return self.queryset.all()
        
        # For update/delete, users can only modify their own reviews
        return self.queryset.filter(reviewer=user)

    def perform_create(self, serializer):
        """Set the reviewer to current user when creating a review"""
        serializer.save(reviewer=self.request.user)