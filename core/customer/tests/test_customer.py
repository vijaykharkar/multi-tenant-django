from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from tenant.models import Tenant_User
from organization.models import Organization
from department.models import Department
from rest_framework.authtoken.models import Token
from django.urls import reverse
from ..models import Customer
from rest_framework.exceptions import ValidationError


class CustomerViewTests(APITestCase):

    def setUp(self):
       
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tenant = Tenant_User.objects.create(tenant_id=1, name="Tenant A", domain="tenanta.com")
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.client.force_authenticate(user=self.user)

        self.set_tenant_header(self.tenant.domain)

        # Create organization and department under this tenant
        self.organization = Organization.objects.create(name="Org A", tenant=self.tenant)
        self.department = Department.objects.create(name="HR", organization=self.organization)

        # URL endpoints
        self.customer_list_url = reverse('customer-list')  # Adjust to your actual URL name
        self.customer_detail_url = lambda customer_id: reverse('customer-detail', kwargs={'id': customer_id})

    def set_tenant_header(self, domain):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key,
                                HTTP_X_TENANT_DOMAIN=domain)

    def test_get_customer_list_success(self):
        # Create customers
        Customer.objects.create(name="John Doe", email="john@example.com", phone="1234567890", department=self.department)
        Customer.objects.create(name="Jane Doe", email="jane@example.com", phone="0987654321", department=self.department)

        response = self.client.get(self.customer_list_url,data={"department": self.department.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_customer_list_no_tenant(self):
        self.set_tenant_header("invalid.com")
        response = self.client.get(self.customer_list_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Tenant not found.")

    def test_create_customer_success(self):
        data = {"name": "New Customer", "email": "newcustomer@example.com", "phone": "1122334455", "department": self.department.name}
        response = self.client.post(self.customer_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Customer")

    def test_create_customer_invalid_department(self):
        invalid_department = "NonExistentDept"
        data = {"name": "Invalid Dept Customer", "email": "invalid@example.com", "phone": "5566778899", "department": invalid_department}
        response = self.client.post(self.customer_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Department does not belong to your tenant or does not exist.")

    def test_create_customer_missing_fields(self):
        response = self.client.post(self.customer_list_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_customer_detail_success(self):
        customer = Customer.objects.create(name="Alice Smith", email="alice@example.com", phone="1231231234", department=self.department)
        response = self.client.get(self.customer_detail_url(customer.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Alice Smith")

    def test_get_customer_detail_invalid_tenant(self):
        customer = Customer.objects.create(name="Bob Brown", email="bob@example.com", phone="9879879876", department=self.department)
        self.set_tenant_header("wrong-tenant.com")
        response = self.client.get(self.customer_detail_url(customer.id))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Tenant not found.")

    def test_get_customer_detail_not_found(self):
        response = self.client.get(self.customer_detail_url(9999))  # Non-existing customer ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

