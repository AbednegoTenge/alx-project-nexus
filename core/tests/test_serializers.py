from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from core.serializer import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    ApplyJobSerializer, JobPostingSerializer, GetJobSerializer
)
from core.models import CandidateProfile, JobPosting, EmployerProfile, Application, Category
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import MagicMock
from decimal import Decimal

User = get_user_model()

class UserSerializerTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
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
            'email': 'newuser@example.com',
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
        self.assertIn('non_field_errors', serializer.errors) 
        # Note: Depending on how ValidationError is raised, it might be in non_field_errors or a specific field.
        # In the code: raise serializers.ValidationError({'detail': 'Passwords do not match'}, code=400)
        # It's a dict, so it might be under 'detail' if DRF passes it through, or non_field_errors.
        # Let's check the error content if needed, but failing validity is key.

class LoginSerializerTest(TestCase):
    def setUp(self):
        self.password = 'password123'
        self.user = User.objects.create_user(email='test@example.com', password=self.password)
        self.login_data = {
            'email': 'test@example.com',
            'password': self.password
        }

    def test_login_serializer_valid(self):
        # We need to mock the request in context because authenticate uses it
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
        # authenticate will return None
        # validation should fail
        # The serializer raises ValidationError manually in validate
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class JobPostingSerializerTest(TestCase):
    def setUp(self):
        self.employer_user = User.objects.create_user(email='employer@example.com', password='password', role=User.Role.EMPLOYER)
        # Create EmployerProfile
        self.employer_profile = EmployerProfile.objects.create(
            user=self.employer_user,
            company_name="Test Company",
            is_verified=True
        )
        self.job_data = {
            'title': 'Software Engineer',
            'description': 'Write code',
            'requirements': ['Python', 'Django'],
            'responsibilities': ['Develop', 'Test'],
            'experience_level': JobPosting.ExperienceLevel.SENIOR,
            'employment_type': JobPosting.EmploymentType.FULL_TIME,
            'job_type': JobPosting.LocationType.REMOTE,
            # 'status' defaults to DRAFT usually, but explicit here if needed
            'salary_min': 100000,
            'salary_max': 150000,
        }
        self.request = MagicMock()
        self.request.user = self.employer_user

    def test_job_posting_serializer_create(self):
        serializer = JobPostingSerializer(data=self.job_data, context={'request': self.request})
        # Note: There is a potential bug in JobPostingSerializer.validate regarding employer_profile check
        # validation logic:
        # employer_profile = request.user.is_employer (boolean)
        # if not employer_profile.is_verified: (AttributeError)
        # I suspect this will fail. I will write the test to expect success, and if it fails, I will fix the serializer.
        
        try:
            self.assertTrue(serializer.is_valid())
            job = serializer.save(employer=self.employer_profile) 
            # Note: create() in serializer is JobPosting.objects.create(**validated_data). 
            # It doesn't automatically attach the employer unless passed in save() or implicitly handled.
            # The serializer doesn't strictly handle 'employer' field in 'fields' or 'create'.
            # Modifying the test to pass employer in save() or fix serializer to get it from user.
            
            self.assertEqual(job.title, self.job_data['title'])
            self.assertEqual(job.employer, self.employer_profile)
        except AttributeError:
             print("Caught expected AttributeError in JobPostingSerializer due to bug")
             # Making test fail if bug is present so I know to fix it
             self.fail("JobPostingSerializer has a bug accessing is_verified on a boolean")

class ApplyJobSerializerTest(TestCase):
    def setUp(self):
        self.candidate_user = User.objects.create_user(email='candidate@example.com', password='password', role=User.Role.CANDIDATE)
        self.candidate_profile = CandidateProfile.objects.create(
            user=self.candidate_user,
            is_verified=True,
            first_name='Jane',
            last_name='Doe'
        )
        
        self.employer_user = User.objects.create_user(email='emp@example.com', password='password', role=User.Role.EMPLOYER)
        self.employer_profile = EmployerProfile.objects.create(user=self.employer_user, company_name="Co", is_verified=True)
        
        self.job = JobPosting.objects.create(
            employer=self.employer_profile,
            title='Dev',
            description='Desc',
            status=JobPosting.Status.ACTIVE,
            experience_level=JobPosting.ExperienceLevel.ENTRY,
            employment_type=JobPosting.EmploymentType.FULL_TIME,
            job_type=JobPosting.LocationType.REMOTE,
            salary_min=50,
            salary_max=100
        )
        # Manually set is_active = True for the job since serializer checks it
        # Model has is_active but status is also checked.
        # JobPostingSerializer checks: job.status != JobPosting.Status.ACTIVE or not job.is_active
        
        self.resume_file = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")

    def test_apply_job_serializer_valid(self):
        data = {
            'cover_letter': 'Hello',
            'resume': self.resume_file
        }
        request = MagicMock()
        request.user = self.candidate_user
        
        context = {'request': request, 'job': self.job, 'candidate_profile': self.candidate_profile}
        
        serializer = ApplyJobSerializer(data=data, context=context)
        self.assertTrue(serializer.is_valid())
        application = serializer.save()
        
        self.assertEqual(application.job, self.job)
        self.assertEqual(application.candidate, self.candidate_profile)
