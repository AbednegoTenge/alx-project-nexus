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


class ApplyJObSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['id', 'job_posting', 'candidate', 'cover_letter', 'resume']

    def validate(self, attrs):
        request = self.context.get('request')
        job_posting = self.context.get('job_posting')

        if not request.user.is_candidate:
            raise serializers.ValidationError("Only candidates can apply for job")
        
        if job_posting.status != JobPosting.status.ACTIVE or not job_posting.is_active:
            raise serializers.ValidationError("This job is no more acepting applications")

        # Prevents application duplicates
        if Application.objects.filter(
            job=job_posting,
            candidate=request.user.candidate
        ).exists():
            raise serializers.ValidationError("You have already applied for this job")

        return attrs
