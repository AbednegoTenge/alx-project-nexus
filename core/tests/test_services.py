import pytest
from core.models import User, CandidateProfile, JobPosting, EmployerProfile, Application, Notification, SavedJob
from core.services import DashboardService
from django.utils import timezone

@pytest.mark.django_db
class TestDashboardService:
    def test_get_candidate_dashboard_structure(self):
        # Setup User
        user = User.objects.create_user(email='candidate@example.com', password='password', role='CANDIDATE', first_name='John', last_name='Doe')
        profile = user.candidate
        profile.headline = "Dev"
        profile.phone = "123"
        profile.save()
        
        # Setup Employer & Job
        employer_user = User.objects.create_user(email='employer@example.com', password='password', role='EMPLOYER')
        employer_profile = employer_user.employer_profile
        employer_profile.company_name = 'Tech Corp'
        employer_profile.save()
        job1 = JobPosting.objects.create(
            employer=employer_profile, 
            title='Software Engineer', 
            description='Code stuff',
            job_type='FULL_TIME',
            experience_level='SENIOR',
            salary_min=1000,
            salary_max=2000
        )
        job2 = JobPosting.objects.create(
            employer=employer_profile, 
            title='DevOps', 
            description='Ops stuff', 
            job_type='FULL_TIME', 
            experience_level='ENTRY',
            salary_min=1000,
            salary_max=2000
        )
        
        # Setup Applications
        Application.objects.create(job=job1, candidate=profile, status='PENDING')
        Application.objects.create(job=job2, candidate=profile, status='INTERVIEW')
        
        # Setup Notification
        Notification.objects.create(user=user, title='Welcome', content='Hi', notification_type='SYSTEM')
        
        # Setup SavedJob
        SavedJob.objects.create(candidate=profile, job=job1)
        
        # Call Service
        data = DashboardService.get_candidate_dashboard(user)
        
        # Assertions
        assert data['status'] == 'active'
        assert data['profile']['name'] == 'John Doe'
        assert data['stats']['applications']['total'] == 2
        assert data['stats']['applications']['pending'] == 1
        assert data['stats']['applications']['interview'] == 1
        assert data['stats']['notifications']['total'] == 1
        assert data['stats']['saved_jobs_count'] == 1

    def test_get_candidate_dashboard_no_profile(self):
        # Create user without candidate profile
        user = User.objects.create_user(email='newbie@example.com', password='password', role='CANDIDATE', first_name='New', last_name='User')
        
        data = DashboardService.get_candidate_dashboard(user)
        
        # Should now return active status with empty stats
        assert data['status'] == 'active'
        assert data['profile']['name'] == 'New User'
        assert data['stats']['applications']['total'] == 0
        assert data['stats']['saved_jobs_count'] == 0
