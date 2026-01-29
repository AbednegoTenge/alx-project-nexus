from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db import transaction
from .models import (
    User, Application, JobPosting, CandidateProfile, EmployerProfile,
    CandidateSkill, Education, Certification, Address, Skill
)
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
        extra_kwargs = {
            'job': {'read_only': True},
            'candidate': {'read_only': True}
        }

    def validate(self, attrs):
        request = self.context.get('request')
        job = self.context.get('job')

        candidate_profile = request.user.candidate

        if not candidate_profile:
            raise serializers.ValidationError("Only candidates can apply for job")

        
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
            allowed_extensions = [".pdf", ".doc", ".docx"]
            file_extension = os.path.splitext(resume.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise serializers.ValidationError("Resume file must be a PDF, DOC, or DOCX file")
        return attrs

    def create(self, validated_data):
        job = self.context.get('job')
        candidate_profile = self.context.get('request').user.candidate
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
        if not request.user.is_employer:
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


    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance


class GetJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'status', 'description', 
            'requirements', 'responsibilities', 'nice_to_have', 'job_type', 
            'employment_type', 'experience_level', 'salary_min', 'salary_max', 'benefits', 
            'city', 'country', 'applications_count', 'application_deadline', 'created_at', 'updated_at'
            ]


# ============= Nested Serializers (must come before CandidateProfileSerializer) =============

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'category', 'description']


class CandidateSkillSerializer(serializers.ModelSerializer):
    skill_id = serializers.IntegerField(write_only=True)
    skill = SkillSerializer(read_only=True)
    
    class Meta:
        model = CandidateSkill
        fields = ['id', 'skill_id', 'skill', 'proficiency_level']
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution', 'level', 'field_of_study', 'start_date', 'end_date', 'description']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'description': {'required': False}
        }

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError(
                "End date cannot be before start date"
            )
        return attrs


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['id', 'name', 'issuing_organization', 'issue_date', 'expiry_date', 'credential_id', 'credential_url']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'credential_id': {'required': False},
            'credential_url': {'required': False},
            'expiry_date': {'required': False}
        }

    def validate(self, attrs):
        issue_date = attrs.get('issue_date')
        expiry_date = attrs.get('expiry_date')
        
        if issue_date and expiry_date and expiry_date < issue_date:
            raise serializers.ValidationError(
                "Expiry date cannot be before issue date"
            )
        return attrs


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'country', 'postal_code']
        extra_kwargs = {
            'id': {'read_only': False, 'required': False},
            'street': {'required': False},
            'state': {'required': False},
            'postal_code': {'required': False}
        }


# ============= Profile Serializers =============

class CandidateProfileSerializer(serializers.ModelSerializer):
    """Serializer for candidate profile (read and update)"""
    # Read-only fields
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    picture = serializers.SerializerMethodField(read_only=True)
    resume_url = serializers.SerializerMethodField(read_only=True)
    social_links = serializers.SerializerMethodField(read_only=True)
    
    # Nested fields for read/write
    skills = CandidateSkillSerializer(many=True, required=False, source='candidate_skills')
    education = EducationSerializer(many=True, required=False)
    certifications = CertificationSerializer(many=True, required=False)
    address = AddressSerializer(many=True, required=False)
    
    # Writable fields for social links
    linkedin = serializers.URLField(required=False, allow_blank=True, write_only=True)
    github = serializers.URLField(required=False, allow_blank=True, write_only=True)
    twitter = serializers.URLField(required=False, allow_blank=True, write_only=True)
    website = serializers.URLField(required=False, allow_blank=True, write_only=True)
    
    # File fields
    profile_picture = serializers.ImageField(required=False, write_only=True)
    resume = serializers.FileField(required=False, write_only=True)
    
    class Meta:
        model = CandidateProfile
        fields = [
            # Read-only display fields
            'picture', 'name', 'email', 'social_links', 'resume_url',
            # Writable fields
            'phone', 'gender', 'date_of_birth', 'headline', 'about',
            'linkedin', 'github', 'twitter', 'website',
            'profile_picture', 'resume',
            # Nested fields
            'skills', 'education', 'certifications', 'address'
        ]
        extra_kwargs = {
            'phone': {'required': False},
            'gender': {'required': False},
            'date_of_birth': {'required': False},
            'headline': {'required': False},
            'about': {'required': False},
        }

    def get_picture(self, obj):
        return obj.profile_picture.url if obj.profile_picture else None

    def get_resume_url(self, obj):
        return obj.resume.url if obj.resume else None

    def get_social_links(self, obj):
        return {
            'linkedin': obj.linkedin or '',
            'github': obj.github or '',
            'twitter': obj.twitter or '',
            'website': obj.website or '',
        }

    def validate_resume(self, value):
        """Validate resume file"""
        if value:
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    "Resume file size should not exceed 5MB"
                )
            
            allowed_extensions = ['.pdf', '.doc', '.docx']
            file_extension = os.path.splitext(value.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise serializers.ValidationError(
                    "Resume file must be a PDF, DOC, or DOCX file"
                )
        return value

    def validate_profile_picture(self, value):
        """Validate profile picture"""
        if value:
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError(
                    "Profile picture size should not exceed 2MB"
                )
            
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            file_extension = os.path.splitext(value.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise serializers.ValidationError(
                    "Profile picture must be a JPG, JPEG, PNG, or GIF file"
                )
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        # Extract nested data
        skills_data = validated_data.pop('candidate_skills', None)
        education_data = validated_data.pop('education', None)
        certifications_data = validated_data.pop('certifications', None)
        address_data = validated_data.pop('address', None)

        # Update simple fields
        for field, value in validated_data.items():
            setattr(instance, field, value)
        
        instance.save()

        # Update skills
        if skills_data is not None:
            CandidateSkill.objects.filter(candidate=instance).delete()
            for skill_data in skills_data:
                CandidateSkill.objects.create(
                    candidate=instance,
                    skill_id=skill_data['skill_id'],
                    proficiency_level=skill_data.get('proficiency_level', 'INTERMEDIATE')
                )

        # Update education
        if education_data is not None:
            Education.objects.filter(candidate=instance).delete()
            for edu_data in education_data:
                Education.objects.create(candidate=instance, **edu_data)

        # Update certifications
        if certifications_data is not None:
            Certification.objects.filter(candidate=instance).delete()
            for cert_data in certifications_data:
                Certification.objects.create(candidate=instance, **cert_data)

        # Update addresses
        if address_data is not None:
            Address.objects.filter(candidate=instance).delete()
            for addr_data in address_data:
                Address.objects.create(candidate=instance, **addr_data)

        return instance


class EmployerProfileSerializer(serializers.ModelSerializer):
    """Serializer for employer profile (read and update)"""
    # Read-only computed fields
    name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    company_logo_url = serializers.SerializerMethodField(read_only=True)
    
    # Writable fields
    logo = serializers.ImageField(required=False, write_only=True)
    
    class Meta:
        model = EmployerProfile
        fields = [
            # Read-only fields
            'id', 'name', 'email', 'company_logo_url', 'is_verified',
            # Writable fields
            'company_name', 'logo', 'industry', 'city', 'country', 
            'description', 'website_url', 'linkedin_url'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'is_verified': {'read_only': True},
            'company_name': {'required': False},
            'industry': {'required': False},
            'city': {'required': False},
            'country': {'required': False},
            'description': {'required': False},
            'website_url': {'required': False, 'allow_blank': True},
            'linkedin_url': {'required': False, 'allow_blank': True},
        }

    def get_company_logo_url(self, obj):
        """Return company logo URL"""
        return obj.logo.url if obj.logo else None

    def validate_logo(self, value):
        """Validate company logo"""
        if value:
            # Check file size (2MB limit)
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError(
                    "Logo size should not exceed 2MB"
                )
            
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
            file_extension = os.path.splitext(value.name)[1].lower()
            if file_extension not in allowed_extensions:
                raise serializers.ValidationError(
                    "Logo must be a JPG, JPEG, PNG, GIF, or SVG file"
                )
        return value

    def validate_website_url(self, value):
        """Validate website URL format"""
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError(
                "Website URL must start with http:// or https://"
            )
        return value

    def validate_linkedin_url(self, value):
        """Validate LinkedIn URL"""
        if value and 'linkedin.com' not in value.lower():
            raise serializers.ValidationError(
                "Please provide a valid LinkedIn URL"
            )
        return value

    def update(self, instance, validated_data):
        """Update employer profile"""
        # Update all fields
        for field, value in validated_data.items():
            setattr(instance, field, value)
        
        instance.save()
        return instance