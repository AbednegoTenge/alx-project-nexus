import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from core.models import Application, JobPosting

User = get_user_model()

@pytest.mark.django_db
def test_login_endpoint():
    client = APIClient()

    # create a test user
    User.objects.create_user(
        email='testuser@example.com',
        first_name='Test',
        last_name='User',
        password='testpassword',
        role='CANDIDATE'
    )

    # make a login request
    url = reverse('auth-login')
    data = {
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }
    response = client.post(url, data)

    assert response.status_code == 200
    assert 'refresh' in response.data
    assert 'access' in response.data


@pytest.mark.django_db
def test_register_endpoint():
    client = APIClient()

    url = reverse('auth-register')
    data = {
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpassword',
        'confirm_password': 'testpassword',
        'role': 'CANDIDATE'
    }
    response = client.post(url, data, format='json')

    assert response.status_code == 201



@pytest.mark.django_db
def test_me_endpoint_authenticated():
    client = APIClient()
    user = User.objects.create_user(email='me@example.com', password='password', role='CANDIDATE')
    
    # Create profile and data
    # Create profile and data
    employer_user = User.objects.create_user(email='emp@example.com', password='password', role='EMPLOYER')
    employer_profile = employer_user.employer_profile
    employer_profile.company_name = 'Co'
    employer_profile.save()
    
    job = JobPosting.objects.create(employer=employer_profile, title='Job', description='Desc', salary_min=10, salary_max=20)
    profile = user.candidate
    Application.objects.create(candidate=profile, job=job)

    client.force_authenticate(user=user)
    
    url = reverse('auth-me')
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data['user']['email'] == 'me@example.com'

@pytest.mark.django_db
def test_me_endpoint_unauthenticated():
    client = APIClient()
    url = reverse('auth-me')
    response = client.get(url)
    
    assert response.status_code == 401