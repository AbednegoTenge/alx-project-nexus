from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from core.serializer import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    ApplyJobSerializer, JobPostingSerializer
)
from core.models import CandidateProfile, JobPosting, EmployerProfile
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import MagicMock

User = get_user_model()

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@yahoo.org',
            'password': 'password123',
            'role': User.Role.CANDIDATE
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_serializer_contains_expected_fields(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(start_set(data.keys()), {'id', 'email', 'role'})
        self.assertEqual(data['email'], self.user_data['email'])
        self.assertEqual(data['role'], self.user_data['role'])

def start_set(keys):
    return set(keys)

class RegisterSerializerTest(TestCase):
    def setUp(self):
        self.register_data = {
            'email': 'newuser@yahoo.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'confirm_password': 'password123',
            'role': User.Role.CANDIDATE
        }

    def test_register_serializer_valid(self):
        serializer = RegisterSerializer(data=self.register_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, self.register_data['email'])
        self.assertTrue(user.check_password(self.register_data['password']))

    def test_register_serializer_password_mismatch(self):
        data = self.register_data.copy()
        data['confirm_password'] = 'mismatch'
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        errors_str = str(serializer.errors)
        self.assertIn('Passwords do not match', errors_str)

class LoginSerializerTest(TestCase):
    def setUp(self):
        self.password = 'password123'
        self.user = User.objects.create_user(email='test@yahoo.org', password=self.password, role=User.Role.CANDIDATE)
        self.user.is_active = True
        self.user.save()
        self.login_data = {
            'email': 'test@yahoo.org',
            'password': self.password
        }

    def test_login_serializer_valid(self):
        request = MagicMock()
        serializer = LoginSerializer(data=self.login_data, context={'request': request})
        self.assertTrue(serializer.is_valid())
        result = serializer.validated_data
        self.assertEqual(result['user'], self.user)
        self.assertIn('access', result)
        self.assertIn('refresh', result)

    def test_login_serializer_invalid_credentials(self):
        data = self.login_data.copy()
        data['password'] = 'wrongpass'
        request = MagicMock()
        serializer = LoginSerializer(data=data, context={'request': request})
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class JobPostingSerializerTest(TestCase):
    def setUp(self):
        # Create employer user
        self.employer_user = User.objects.create_user(
            email='employer@yahoo.org', 
            password='password', 
            role=User.Role.EMPLOYER
        )
        
        # Get the employer profile that was auto-created
        self.employer_profile = EmployerProfile.objects.get(user=self.employer_user)
        
        self.job_data = {
            'title': 'Software Engineer',
            'description': 'Write code',
            'requirements': ['Python', 'Django'],
            'responsibilities': ['Develop', 'Test'],
            'experience_level': JobPosting.ExperienceLevel.SENIOR,
            'employment_type': JobPosting.EmploymentType.FULL_TIME,
            'job_type': JobPosting.LocationType.REMOTE,
            'status': JobPosting.Status.ACTIVE,
            'salary_min': 100000,
            'salary_max': 150000,
        }
        
        # Create a proper mock request with employer_profile
        self.request = MagicMock()
        self.request.user = self.employer_user
        self.request.user.employer_profile = self.employer_profile

    def test_job_posting_serializer_create(self):
        serializer = JobPostingSerializer(data=self.job_data, context={'request': self.request})
        
        # Debug: print errors if not valid
        if not serializer.is_valid():
            print("JobPosting Serializer errors:", serializer.errors)
        
        self.assertTrue(serializer.is_valid())
        job = serializer.save()
        
        self.assertEqual(job.title, self.job_data['title'])
        # Fix: employer is an EmployerProfile, not a User
        self.assertEqual(job.employer, self.employer_profile)
        self.assertEqual(job.posted_by, self.employer_profile)

class ApplyJobSerializerTest(TestCase):
    def setUp(self):
        # Create candidate user
        self.candidate_user = User.objects.create_user(
            email='candidate@yahoo.org', 
            password='password', 
            role=User.Role.CANDIDATE
        )
        self.candidate_user.first_name = 'Jane'
        self.candidate_user.last_name = 'Doe'
        self.candidate_user.save()

        # Get the auto-created candidate profile
        self.candidate_profile = CandidateProfile.objects.get(user=self.candidate_user)
        
        # Create employer user and profile
        self.employer_user = User.objects.create_user(
            email='emp@yahoo.com', 
            password='password', 
            role=User.Role.EMPLOYER
        )
        self.employer_profile = EmployerProfile.objects.get(user=self.employer_user)
        
        # Create job posting
        self.job = JobPosting.objects.create(
            employer=self.employer_profile,
            posted_by=self.employer_profile,
            title='Dev',
            description='Desc',
            status=JobPosting.Status.ACTIVE,
            experience_level=JobPosting.ExperienceLevel.ENTRY,
            employment_type=JobPosting.EmploymentType.FULL_TIME,
            job_type=JobPosting.LocationType.REMOTE,
            salary_min=50,
            salary_max=100,
            requirements=['Python'],
            responsibilities=['Code']
        )
        
        self.resume_file = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")

    def test_apply_job_serializer_valid(self):
        # ApplyJobSerializer expects job and candidate from context, not data
        data = {
            'cover_letter': 'Hello',
            'resume': self.resume_file,
        }
        
        # Create proper mock request
        request = MagicMock()
        request.user = self.candidate_user
        request.user.candidate_profile = self.candidate_profile
        
        # Pass job and candidate_profile in context (based on your view implementation)
        context = {
            'request': request,
            'job': self.job
        }
        
        serializer = ApplyJobSerializer(data=data, context=context)
        
        # Debug: print errors if not valid
        if not serializer.is_valid():
            print("ApplyJob Serializer errors:", serializer.errors)
        
        self.assertTrue(serializer.is_valid())
        application = serializer.save()
        
        self.assertEqual(application.job, self.job)
        self.assertEqual(application.candidate, self.candidate_profile)