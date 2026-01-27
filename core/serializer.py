from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Application, JobPosting


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

        if not request.user.is_candidate:
            raise serializers.ValidationError("Only candidates can apply for job")
        
        if job.status != JobPosting.Status.ACTIVE or not job.is_active:
            raise serializers.ValidationError("This job is no more acepting applications")

        # Prevents application duplicates
        if Application.objects.filter(
            job=job,
            candidate=request.user.candidate
        ).exists():
            raise serializers.ValidationError("You have already applied for this job")

        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        job = self.context.get('job')

        return Application.objects.create(
            job=job,
            candidate=request.user.candidate,
            **validated_data
        )

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = ['id', 'title', 'description', 'status', 'created_at', 'updated_at']

    def validate(self, attrs):
        request = self.context.get('request')
        if not request.user.is_employer:
            raise serializers.ValidationError("Only employers can create job postings")
        return attrs

    def create(self, validated_data):
        return JobPosting.objects.create(**validated_data)

class GetJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = [
            'id', 'title', 'status', 'description', 
            'requirements', 'responsibilities', 'nice_to_have', 'job_type', 
            'experience_level', 'salary_min', 'salary_max', 'benefits', 'is_remote', 
            'is_hybrid', 'city', 'country', 'applications_count', 'application_deadline', 'created_at', 'updated_at'
            ]