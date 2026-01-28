from django.db.models import Count, Avg
from django.utils import timezone
from django.utils.timezone import timedelta
from django.db.models import Q


class DashboardService:
    """Service class for handling dashboard data"""

    @staticmethod
    def get_dashboard(user):
        """Return role based dashboard data"""
        if user.is_candidate:
            return DashboardService.get_candidate_dashboard(user)
        elif user.is_employer:
            return DashboardService.get_employer_dashboard(user)
        else:
            return {
                "status": "error",
                "message": "User role not recognized"
            }
        

    @staticmethod
    def get_candidate_dashboard(user):
        """Return candidate dashboard data"""
        from .models import (
            Application, Notification, SavedJob, 
            CandidateSkill, Education, Certification,
            Address
        )
        from django.core.exceptions import ObjectDoesNotExist
        
        try:
            profile = user.candidate
        except ObjectDoesNotExist:
            return {
                'status': 'error',
                'message': 'Candidate profile not found'
            }
            
        # Application Stats
        applications = Application.objects.filter(candidate=profile)
        total_applications = applications.count()
        
        # Status Breakdown
        status_counts = {
            'total': total_applications,
            'pending': applications.filter(status=Application.Status.PENDING).count(),
            'reviewed': applications.filter(status=Application.Status.REVIEWED).count(),
            'shortlisted': applications.filter(status=Application.Status.SHORTLISTED).count(),
            'interview': applications.filter(status=Application.Status.INTERVIEW).count(),
            'rejected': applications.filter(status=Application.Status.REJECTED).count(),
            'accepted': applications.filter(status=Application.Status.ACCEPTED).count(),
        }
        
        # Recent Activity (Last 5 applications)
        recent_apps_data = list(
            applications.select_related('job', 'job__employer')
            .order_by('-applied_at')[:5]
            .values(
                'id', 'job__title', 'job__employer__company_name', 'applied_at', 'status', 'job__employer__logo'
            )
        )

        # Skills
        skills = CandidateSkill.objects.filter(candidate=profile).select_related('skill')
        skills_data = list(skills.values(
            'id', 'skill__name', 'skill__category', 'skill__description'
        ))

        # Education
        education_data = list(Education.objects.filter(candidate=profile).values(
            'id', 'institution', 'level', 'field_of_study', 'start_date', 'end_date',
        ))

        # Certifications
        certifications_data = list(Certification.objects.filter(candidate=profile).values(
            'id', 'name', 'issuing_organization', 'issue_date', 'expiry_date'
        ))

        # Notifications (User based, so works without profile)
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        unread_count = notifications.filter(is_read=False).count()
        recent_notifications = notifications[:5]
        notifications_data = list(recent_notifications.values(
            'id', 'title', 'notification_type', 'created_at', 'is_read'
        ))

        address = Address.objects.filter(user=user)
        address_data = list(address.values(
            'id', 'street', 'city', 'state', 'postal_code', 'country'
        ))

        # Saved Jobs
        if profile:
            saved_job_qs = SavedJob.objects.filter(candidate=profile)
            saved_jobs = saved_job_qs.select_related('job', 'job__employer').order_by('-created_at')[:5]
            saved_jobs_count = saved_job_qs.count()
        else:
            saved_jobs = []
            saved_jobs_count = 0

        saved_jobs_data = list(saved_jobs.values(
            'id', 'job__title', 'job__employer__company_name', 'created_at', 'job__employer__logo'
        ))

        return {
            "status": "active",
            "profile": {
                "picture": profile.profile_picture if profile.profile_picture else None,
                "name": user.get_full_name(),
                "email": user.email,
                "phone": profile.phone,
                "gender": profile.gender,
                "date_of_birth": profile.date_of_birth,
                "headline": profile.headline if profile else "",
                "about": profile.about,
                "social_links": {
                    "linkedin": profile.linkedin,
                    "github": profile.github,
                    "twitter": profile.twitter,
                    "website": profile.website,
                },
                "resume": profile.resume if profile.resume else None,
                "skills": skills_data,
                "education": education_data,
                "certifications": certifications_data,
                "address": address_data,
            },
            "stats": {
                "applications": status_counts,
                "notifications": {
                    "unread": unread_count,
                    "total": notifications.count()
                },
                "saved_jobs_count": saved_jobs_count
            },
            "recent_applications": recent_apps_data,
            "recent_notifications": notifications_data,
            "saved_jobs": saved_jobs_data
        }    
        

    def get_employer_dashboard(user):
        """Dashboard data for employers"""
        from .models import EmployerProfile, JobPosting, Application, CompanyReview
        
        try:
            profile = user.employer_profile
        except EmployerProfile.DoesNotExist:
            return {
                'profile_exists': False,
                'message': 'Please complete your company profile to get started'
            }
        
        # Get all jobs posted by this employer
        jobs = JobPosting.objects.filter(employer=profile, is_active=True)
        
        # Active jobs
        active_jobs = jobs.filter(status='ACTIVE')
        
        # All applications for this employer's jobs
        all_applications = Application.objects.filter(
            job__employer=profile,
            is_active=True
        )
        
        # Recent applications (last 10)
        recent_applications = all_applications.select_related(
            'candidate__user', 
            'job'
        ).order_by('-applied_at')[:10]
        
        # Applications by status
        applications_by_status = all_applications.values('status').annotate(count=Count('id'))
        
        # Top performing jobs (by applications)
        top_jobs = active_jobs.annotate(
            app_count=Count('applications', filter=Q(applications__is_active=True))
        ).order_by('-app_count')[:5]
        
        # Jobs expiring soon (within 7 days)
        expiring_soon = active_jobs.filter(
            application_deadline__lte=timezone.now() + timedelta(days=7),
            application_deadline__gte=timezone.now()
        ).count()
        
        # Recent notifications
        from .models import Notification
        unread_notifications = Notification.objects.filter(
            user=user,
            is_read=False,
            is_active=True
        ).count()
        
        # Company reviews
        reviews = CompanyReview.objects.filter(company=profile, is_active=True)
        avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        
        return {
            'profile_exists': True,
            'company': {
                'id': profile.id,
                'company_name': profile.company_name,
                'logo': profile.logo.url if profile.logo else None,
                'industry': profile.industry or '',
                'is_verified': profile.is_verified,
                'city': profile.city or '',
                'country': profile.country or '',
            },
            'statistics': {
                'total_jobs': jobs.count(),
                'active_jobs': active_jobs.count(),
                'draft_jobs': jobs.filter(status='DRAFT').count(),
                'closed_jobs': jobs.filter(status='CLOSED').count(),
                'total_applications': all_applications.count(),
                'pending_applications': all_applications.filter(status='PENDING').count(),
                'shortlisted_candidates': all_applications.filter(status='SHORTLISTED').count(),
                'jobs_expiring_soon': expiring_soon,
                'unread_notifications': unread_notifications,
                'average_rating': round(float(avg_rating), 1),
                'total_reviews': reviews.count(),
            },
            'applications_by_status': {
                item['status']: item['count'] 
                for item in applications_by_status
            },
            'recent_applications': [
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
                for app in recent_applications
            ],
            'top_performing_jobs': [
                {
                    'id': job.id,
                    'title': job.title,
                    'applications_count': job.app_count,
                    'location': job.location or '',
                    'posted_at': job.posted_at.isoformat() if job.posted_at else None,
                    'status': job.status,
                }
                for job in top_jobs
            ],
        }