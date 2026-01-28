from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Application, JobPosting
import os


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # auhenticate user
        user = authenticate(
            request = self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError({'detail': 'Invalid credentials'}, code=400)

        if not user.is_active:
            raise serializers.ValidationError({'detail': 'User is not active'}, code=400)

        # generate JWT tokens
        refresh = RefreshToken.for_user(user)

        refresh['email'] = user.email
        refresh['role'] = user.role

        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'confirm_password', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'detail': 'Passwords do not match'}, code=400)
        return attrs

    def create(self, validated_data):
        # pop confirm_password from validated_data
        password = validated_data.pop('confirm_password')
        user = User(**validated_data)
        user.set_password(password) # hash password
        user.save()
        return user
        

class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class ApplyJobSerializer(serializers.ModelSerializer):
    resume = serializers.FileField(required=False)
    class Meta:
        model = Application
        fields = ['id', 'job', 'candidate', 'cover_letter', 'resume']

    def validate(self, attrs):
        request = self.context.get('request')
        job = self.context.get('job')

        candidate_profile = request.user.candidate

        if not candidate_profile:
            raise serializers.ValidationError("Only candidates can apply for job")

        if not candidate_profile.is_verified:
            raise serializers.ValidationError("Please verify your profile before applying for a job")
        
        if job.status != JobPosting.Status.ACTIVE or not job.is_active:
            raise serializers.ValidationError("This job is no more acepting applications")

        # Prevents application duplicates
        if Application.objects.filter(
            job=job,
            candidate=candidate_profile
        ).exists():
            raise serializers.ValidationError("You have already applied for this job")

        # validate resume
        resume = attrs.get('resume')
        if resume:
            if resume.size > 5 * 1024 * 1024:
                raise serializers.ValidationError("Resume file size should not exceed 5MB")
            # validate file extension
            allowed_extensions = [".pdf", ".doc", "docx"]
            file_extension = os.path.splitext(resume.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise serializers.ValidationError("Resume file must be a PDF, DOC, or DOCX file")
        return attrs

    def create(self, validated_data):
        job = self.context.get('job')
        candidate_profile = self.context.get('candidate_profile')
        return Application.objects.create(
            job=job,
            candidate=candidate_profile,
            **validated_data
        )

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'description', 'requirements', 'responsibilities', 'experience_level', 'employment_type', 'status', 'job_type', 'created_at', 'updated_at']

    def validate(self, attrs):
        request = self.context.get('request')
        if not hasattr(request.user, 'employer_profile'):
            raise serializers.ValidationError("Only employers can create job postings")

        # validate job title
        title = attrs.get('title')
        if not title:
            raise serializers.ValidationError("Job title is required")

        # validate job description
        description = attrs.get('description')
        if not description:
            raise serializers.ValidationError("Job description is required")

        # validate job requirements
        requirements = attrs.get('requirements')
        if not requirements:
            raise serializers.ValidationError("Job requirements are required")

        # validate job responsibilities
        responsibilities = attrs.get('responsibilities')
        if not responsibilities:
            raise serializers.ValidationError("Job responsibilities are required")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['employer'] = request.user.employer_profile
        validated_data['posted_by'] = request.user.employer_profile
        return JobPosting.objects.create(**validated_data)

class GetJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'status', 'description', 
            'requirements', 'responsibilities', 'nice_to_have', 'job_type', 
            'employment_type', 'experience_level', 'salary_min', 'salary_max', 'benefits', 
            'city', 'country', 'applications_count', 'application_deadline', 'created_at', 'updated_at'
            ]