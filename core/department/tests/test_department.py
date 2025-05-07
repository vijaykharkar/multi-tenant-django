from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from tenant.models import Tenant_User
from organization.models import Organization
from department.models import Department
from rest_framework.authtoken.models import Token
from django.urls import reverse


class DepartmentViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tenant = Tenant_User.objects.create(tenant_id=1, name="Tenant A", domain="tenanta.com")
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.force_authenticate(user=self.user)

        self.set_tenant_header(self.tenant.domain)

        
        self.organization = Organization.objects.create(name="Org A", tenant=self.tenant)

       
        self.department_list_url = reverse('department-list')
        self.department_detail_url = lambda dep_id: reverse('department-detail', kwargs={'id': dep_id})

    def set_tenant_header(self, domain):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key,
                                HTTP_X_TENANT_DOMAIN=domain)

    def test_get_department_list_success(self):
        Department.objects.create(name="HR", organization=self.organization)
        Department.objects.create(name="IT", organization=self.organization)

        response = self.client.get(self.department_list_url, data={"organization": self.organization.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_department_list_no_tenant(self):
        self.set_tenant_header("invalid.com")
        response = self.client.get(self.department_list_url, data={"organization": self.organization.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Tenant not found.")

    def test_create_department_success(self):
        data = {"name": "Finance", "organization": self.organization.id}
        response = self.client.post(self.department_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Finance")

    def test_create_department_invalid_organization(self):
        data = {"name": "Legal", "organization": 9999}
        response = self.client.post(self.department_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Organization does not belong to your tenant or does not exist.")

    def test_create_department_missing_fields(self):
        response = self.client.post(self.department_list_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_department_detail_success(self):
        dep = Department.objects.create(name="Admin", organization=self.organization)
        response = self.client.get(self.department_detail_url(dep.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Admin")

    def test_get_department_detail_invalid_tenant(self):
        dep = Department.objects.create(name="Logistics", organization=self.organization)
        self.set_tenant_header("wrong-tenant.com")
        response = self.client.get(self.department_detail_url(dep.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Tenant not found.")

    def test_get_department_detail_not_found(self):
        response = self.client.get(self.department_detail_url(9999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
