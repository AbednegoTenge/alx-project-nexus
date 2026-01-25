
class DashboardService:
    """Service class for handling dashboard data"""

    @staticmethod
    def get_dashboard(user):
        """Return role based dashboard data"""
        if user.is_candidate:
            return DashboardService.get_candidate_dashboard(user)
        

    @staticmethod
    def get_candidate_dashboard(user):
        """Return candidate dashboard data"""
        from .models import Application, Notification, SavedJob, CandidateSkill, Education, Certification
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
        
    