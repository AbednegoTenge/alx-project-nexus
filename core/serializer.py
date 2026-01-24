from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User


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
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'detail': 'Passwords do not match'}, code=400)
        return attrs

    def create(self, validated_data):
        # pop password2 from validated_data
        password = validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password) # hash password
        user.save()
        return user
        

class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()