import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

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
    url = reverse('login')
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

    url = reverse('register')
    data = {
        'email': 'testuser@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'testpassword',
        'confirm_password': 'testpassword',
        'role': 'CANDIDATE'
    }
    response = client.post(url, data, format='json')
    print(response.data)

    assert response.status_code == 201
