from rest_framework import serializers
from .models import Customer
from department.models import Department

class CustomerSerializer(serializers.ModelSerializer):

    department = serializers.SlugRelatedField(
        queryset=Department.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Customer
        fields = '__all__'
        
