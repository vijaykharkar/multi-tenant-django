from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from ..models import Organization  
from tenant.models import Tenant_User  
from django.urls import reverse
from rest_framework.authtoken.models import Token


class OrganizationViewTests(APITestCase):

    def setUp(self):
       
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tenant = Tenant_User.objects.create(
            tenant_id=6,
            name="Tenant A",
            domain="tenanta.com"
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        
        self.client.force_authenticate(user=self.user)
        self.client.tenant = self.tenant  

        
        self.org_list_url = reverse('organization-list')
        self.org_detail_url = lambda org_id: reverse('organization-detail', kwargs={"id": org_id})

    def set_tenant_header(self, domain):
        """Helper method to set the X-Tenant-Domain header."""
        self.client.credentials(HTTP_X_TENANT_DOMAIN=domain)

    def test_get_organization_list_success(self):
        self.set_tenant_header(self.tenant.domain)
        
        
        Organization.objects.create(name="Org1", tenant=self.tenant)
        Organization.objects.create(name="Org2", tenant=self.tenant)

        response = self.client.get(self.org_list_url,  {"tenant": self.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_organization_list_no_tenant(self):
        self.set_tenant_header("invalid-domain.com")  
        response = self.client.get(self.org_list_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Tenant not found.")

    def test_create_organization_success(self):
        data = {"name": "New Org", "tenant": self.tenant.id}
        response = self.client.post(self.org_list_url, data, HTTP_X_TENANT_DOMAIN=self.tenant.domain)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "New Org")
        self.assertEqual(response.data['tenant'], self.tenant.id)

    def test_create_organization_missing_fields(self):
        data = {}
        response = self.client.post(self.org_list_url, data, HTTP_X_TENANT_DOMAIN=self.tenant.domain)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_organization_detail_success(self):
        org = Organization.objects.create(name="Detail Org", tenant=self.tenant)
        response = self.client.get(self.org_detail_url(org.id), HTTP_X_TENANT_DOMAIN=self.tenant.domain)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Detail Org")

    def test_get_organization_detail_not_found(self):
        response = self.client.get(self.org_detail_url(9999), HTTP_X_TENANT_DOMAIN=self.tenant.domain)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_organization_detail_no_tenant(self):
        org = Organization.objects.create(name="Tenant Org", tenant=self.tenant)
        response = self.client.get(self.org_detail_url(org.id), HTTP_X_TENANT_DOMAIN="invalid-domain.com")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
