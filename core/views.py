from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializer import LoginSerializer, RegisterSerializer, TokenRefreshResponseSerializer, UserSerializer
from .services import DashboardService



class AuthViewSet(ModelViewSet):

    def get_permissions(self):
        if self.action in ['login', 'register']:
            return [AllowAny()]
        return [IsAuthenticated()]

    
    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSerializer
        elif self.action == 'register':
            return RegisterSerializer
        elif self.action == 'refresh':
            return TokenRefreshResponseSerializer
        return LoginSerializer # Default serializer


    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        access_token = serializer.validated_data['access']
        refresh_token = serializer.validated_data['refresh']
        return Response({
            'user': UserSerializer(user).data,
            'access': access_token,
            'refresh': refresh_token,
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        dashboard = DashboardService.get_dashboard(user)
        return Response({
            'user': UserSerializer(user).data,
            'dashboard': dashboard
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)