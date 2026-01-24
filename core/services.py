from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import timedelta


class DashboardService:
    """Service class for handling dashboard data"""

    @staticmethod
    def get_dashboard(user):
        """Return role based dashboard data"""
        if user.is_candidate:
            return DashboardService.get_candidate_dashboard(user)
        elif user.is_employer:
            return DashboardService.get_employer_dashboard(user)
        elif user.is_admin:
            return DashboardService.get_admin_dashboard(user)

    @staticmethod
    def get_candidate_dashboard(user):
        """Return candidate dashboard data"""
        return {
            'total_jobs': user.candidate.job_applications.count(),
            'total_applications': user.candidate.job_applications.count(),
            'total_interviews': user.candidate.job_applications.count(),
        }
    