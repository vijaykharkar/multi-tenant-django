from rest_framework import serializers
from .models import Organization
from tenant.models import Tenant_User

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
