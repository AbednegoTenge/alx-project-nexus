
import pytest
from rest_framework.exceptions import NotFound
from core.models import (
    User, CandidateProfile, JobPosting, EmployerProfile, 
    Application, Notification, SavedJob, CompanyReview
)
from core.services import (
    ProfileService, ApplicationService, 
    SavedJobsService, NotificationService, ReviewService
)
from django.utils import timezone

@pytest.mark.django_db
class TestProfileService:
    def test_get_candidate_profile(self):
        user = User.objects.create_user(email='candidate@test.com', password='password', role='CANDIDATE', first_name='Jane', last_name='Doe')
        # Profile created via signal, update it
        profile = user.candidate
        profile.headline = "Python Dev"
        profile.save()
        
        data = ProfileService.get_profile(user)
        
        assert data['name'] == 'Jane Doe'
        assert data['email'] == 'candidate@test.com'
        assert data['headline'] == 'Python Dev'
        assert 'skills' in data
        assert 'education' in data

    def test_get_employer_profile(self):
        user = User.objects.create_user(email='employer@test.com', password='password', role='EMPLOYER')
        profile = user.employer_profile
        profile.company_name = "Tech Inc"
        profile.save()
        
        data = ProfileService.get_profile(user)
        
        assert data['company_name'] == 'Tech Inc'
        assert 'id' in data

    def test_get_profile_invalid_role(self):
        user = User.objects.create_user(email='admin@test.com', password='password', role='ADMIN')
        with pytest.raises(NotFound):
            ProfileService.get_profile(user)

@pytest.mark.django_db
class TestApplicationService:
    def test_get_candidate_applications(self):
        candidate_user = User.objects.create_user(email='c@test.com', password='pw', role='CANDIDATE')
        employer_user = User.objects.create_user(email='e@test.com', password='pw', role='EMPLOYER')
        employer_profile = employer_user.employer_profile
        
        job = JobPosting.objects.create(
            employer=employer_profile, title="Dev", status="ACTIVE", 
            job_type="FULL_TIME", experience_level="SENIOR"
        )
        
        Application.objects.create(job=job, candidate=candidate_user.candidate)
        
        data = ApplicationService.get_candidate_applications(candidate_user)
        assert len(data) == 1
        assert data[0]['job_title'] == "Dev"

    def test_get_employer_applications(self):
        candidate_user = User.objects.create_user(email='c@test.com', password='pw', role='CANDIDATE')
        employer_user = User.objects.create_user(email='e@test.com', password='pw', role='EMPLOYER')
        employer_profile = employer_user.employer_profile
        
        job = JobPosting.objects.create(
            employer=employer_profile, title="Dev", status="ACTIVE",
            job_type="FULL_TIME", experience_level="SENIOR"
        )
        
        Application.objects.create(job=job, candidate=candidate_user.candidate)
        
        data = ApplicationService.get_employer_applications(employer_user)
        assert len(data) == 1
        assert data[0]['job_title'] == "Dev"

@pytest.mark.django_db
class TestSavedJobsService:
    def test_get_saved_jobs_for_candidate(self):
        candidate_user = User.objects.create_user(email='c@test.com', password='pw', role='CANDIDATE')
        employer_user = User.objects.create_user(email='e@test.com', password='pw', role='EMPLOYER')
        employer_profile = employer_user.employer_profile
        
        job = JobPosting.objects.create(
            employer=employer_profile, title="Dev", status="ACTIVE",
            job_type="FULL_TIME", experience_level="SENIOR"
        )
        
        SavedJob.objects.create(candidate=candidate_user.candidate, job=job)
        
        data = SavedJobsService.get_saved_jobs(candidate_user)
        assert len(data) == 1
        assert data[0]['job_title'] == "Dev"

@pytest.mark.django_db
class TestNotificationService:
    def test_get_notifications(self):
        user = User.objects.create_user(email='u@test.com', password='pw')
        Notification.objects.create(user=user, title="Test", content="Msg", notification_type="SYSTEM")
        
        data = NotificationService.get_notifications(user)
        assert data['unread_count'] == 1
        assert len(data['notifications']) == 1

@pytest.mark.django_db
class TestReviewService:
    def test_get_reviews_for_employer(self):
        candidate_user = User.objects.create_user(email='c@test.com', password='pw', role='CANDIDATE')
        employer_user = User.objects.create_user(email='e@test.com', password='pw', role='EMPLOYER')
        
        CompanyReview.objects.create(
            company=employer_user.employer_profile,
            reviewer=candidate_user,
            rating=5,
            review_text="Great company"
        )
        
        data = ReviewService.get_reviews(employer_user)
        assert len(data) == 1
        assert data[0]['rating'] == 5
