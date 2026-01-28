from rest_framework.exceptions import NotFound
from .models import (
    Application, Notification, SavedJob, 
    CandidateProfile, EmployerProfile, CompanyReview
)


class ApplicationService:
    """Service for retrieving application related data efficiently"""

    @staticmethod
    def get_candidate_applications(user, limit=None):
        try:
            profile = user.candidate
        except CandidateProfile.DoesNotExist:
            raise NotFound("Candidate profile not found")

        # Fetch applications and related job + employer in one go
        qs = Application.objects.filter(candidate=profile, is_active=True) \
            .select_related('job', 'job__employer') \
            .order_by('-applied_at')

        if limit:
            qs = qs[:limit]

        return [
            {
                'id': app.id,
                'job_title': app.job.title,
                'company_name': app.job.employer.company_name,
                'applied_at': app.applied_at.isoformat() if app.applied_at else None,
                'status': app.status,
                'company_logo': app.job.employer.logo.url if app.job.employer.logo else None,
            }
            for app in qs
        ]

    @staticmethod
    def get_employer_applications(user, limit=None):
        try:
            profile = user.employer_profile
        except EmployerProfile.DoesNotExist:
            raise NotFound("Employer profile not found")

        # Fetch applications with related candidate + user + job in one query
        qs = Application.objects.filter(job__employer=profile, is_active=True) \
            .select_related('candidate', 'candidate__user', 'job') \
            .order_by('-applied_at')

        if limit:
            qs = qs[:limit]

        return [
            {
                'id': app.id,
                'candidate_name': app.candidate.user.get_full_name(),
                'candidate_headline': app.candidate.headline or '',
                'candidate_picture': app.candidate.profile_picture.url if app.candidate.profile_picture else None,
                'job_title': app.job.title,
                'status': app.status,
                'applied_at': app.applied_at.isoformat() if app.applied_at else None,
                'expected_salary': float(app.expected_salary) if app.expected_salary else None,
            }
            for app in qs
        ]


class SavedJobsService:
    """Service for retrieving saved jobs efficiently"""

    @staticmethod
    def get_saved_jobs(user, limit=5):
        try:
            profile = user.candidate
        except CandidateProfile.DoesNotExist:
            raise NotFound("Candidate profile not found")

        # Fetch saved jobs with related job + employer in one query
        qs = SavedJob.objects.filter(candidate=profile).select_related('job', 'job__employer').order_by('-created_at')

        if limit:
            qs = qs[:limit]

        return [
            {
                'id': sj.id,
                'job_title': sj.job.title,
                'company_name': sj.job.employer.company_name,
                'created_at': sj.created_at.isoformat() if sj.created_at else None,
                'company_logo': sj.job.employer.logo.url if sj.job.employer.logo else None,
            }
            for sj in qs
        ]

class NotificationService:
    """Service for retrieving notifications"""
    
    @staticmethod
    def get_unread_notifications(user):
        return Notification.objects.filter(user=user, is_read=False).count()

    @staticmethod
    def get_notifications(user, limit=5):
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        unread_count = NotificationService.get_unread_notifications(user)
        
        if limit:
            notifications = notifications[:limit]
            
        data = list(notifications.values('id', 'title', 'notification_type', 'created_at', 'is_read'))
        return {
            "unread_count": unread_count,
            "notifications": data
        }



class ReviewService:
    """Service for retrieving reviews"""
    
    @staticmethod
    def get_reviews(user, limit=5):
        try:
            profile = user.employer_profile
        except EmployerProfile.DoesNotExist:
            raise NotFound("Employer profile not found")
            
        qs = CompanyReview.objects.filter(company=profile).select_related('reviewer').order_by('-created_at')
        
        if limit:
            qs = qs[:limit]
            
        return list(qs.values(
            'id', 
            'reviewer__first_name', 
            'reviewer__last_name', 
            'rating',
            'review_text', 
            'created_at'
        ))