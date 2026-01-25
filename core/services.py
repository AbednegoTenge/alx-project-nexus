
class DashboardService:
    """Service class for handling dashboard data"""

    @staticmethod
    def get_dashboard(user):
        """Return role based dashboard data"""
        if user.is_candidate:
            print(user.is_candidate)
            return DashboardService.get_candidate_dashboard(user)
        

    @staticmethod
    def get_candidate_dashboard(user):
        """Return candidate dashboard data"""
        from .models import Application, Notification, SavedJob
        from django.core.exceptions import ObjectDoesNotExist
        
        try:
            profile = user.candidate
        except ObjectDoesNotExist:
            profile = None
            
        # Application Stats
        if profile:
            applications = Application.objects.filter(candidate=profile)
        else:
            applications = Application.objects.none()
            
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
        recent_applications = applications.select_related('job', 'job__employer').order_by('-applied_at')[:5]
        recent_apps_data = []
        for app in recent_applications:
            recent_apps_data.append({
                'id': app.id,
                'job_title': app.job.title,
                'company': app.job.employer.company_name,
                'applied_at': app.applied_at,
                'status': app.status,
                'status_display': app.get_status_display(),
                'logo_url': app.job.employer.logo.url if app.job.employer.logo else None
            })

        # Notifications (User based, so works without profile)
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        unread_count = notifications.filter(is_read=False).count()
        recent_notifications = notifications[:5]
        notifications_data = []
        for notif in recent_notifications:
            notifications_data.append({
                'id': notif.id,
                'title': notif.title,
                'type': notif.notification_type,
                'created_at': notif.created_at,
                'is_read': notif.is_read
            })

        # Saved Jobs
        if profile:
            saved_job_qs = SavedJob.objects.filter(candidate=profile)
            saved_jobs = saved_job_qs.select_related('job', 'job__employer').order_by('-created_at')[:5]
            saved_jobs_count = saved_job_qs.count()
        else:
            saved_jobs = []
            saved_jobs_count = 0

        saved_jobs_data = []
        for saved in saved_jobs:
            saved_jobs_data.append({
                'id': saved.id,
                'job_title': saved.job.title,
                'company': saved.job.employer.company_name,
                'saved_at': saved.created_at,
                'job_id': saved.job.id,
                'logo_url': saved.job.employer.logo.url if saved.job.employer.logo else None
            })

        return {
            "status": "active",
            "profile": {
                "name": user.get_full_name(),
                "headline": profile.headline if profile else "",
                "avatar": profile.profile_picture.url if profile and profile.profile_picture else None,
                "completeness": 85 if profile else 10, # 10% just for account creation
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
        
    