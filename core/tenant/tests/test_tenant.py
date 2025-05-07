from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import Tenant_User

class TenantTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass123", email="test@example.com")
        self.token = Token.objects.create(user=self.user)
        self.auth_headers = {'HTTP_AUTHORIZATION': f'Token {self.token.key}'}

    def test_register_user(self):
        response = self.client.post('/register/', {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('data', response.data)

    def test_login_user(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)

    def test_create_tenant(self):
        data = {
            "tenant_id": 123,
            "name": "Tenant1",
            "domain": "tenant1.com"
        }
        response = self.client.post('/api/tenant/', data, **self.auth_headers)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Tenant1')

    def test_list_tenants(self):
        Tenant_User.objects.create(tenant_id=123, name="TenantX", domain="tenantx.com")
        response = self.client.get('/api/tenant/', **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_get_tenant_detail(self):
        tenant = Tenant_User.objects.create(tenant_id=123, name="TenantY", domain="tenanty.com")
        response = self.client.get(f'/api/tenant/{tenant.id}/', **self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'TenantY')

    def test_register_user_with_existing_username(self):
        response = self.client.post('/register/', {
            'username': 'testuser',
            'email': 'uniqueemail@example.com',
            'password': 'newpass'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already exists.', str(response.data))

    def test_register_user_with_existing_email(self):
        response = self.client.post('/register/', {
            'username': 'uniqueuser',
            'email': 'test@example.com',
            'password': 'newpass'
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email already exists.', str(response.data))
