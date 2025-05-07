from rest_framework import serializers
from .models import Department
from organization.models import Organization

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
