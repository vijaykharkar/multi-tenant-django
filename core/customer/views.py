from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from department.models import Department 
# from core.permissions import IsTenantUser

class CustomerListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not self.request.tenant:
            return Response({"error": "Tenant not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        department_id = request.query_params.get('department')

        
        if department_id:
            customers = Customer.objects.filter(
                department_id=department_id,
                department__organization__tenant=self.request.tenant
            )
        else:
            customers = Customer.objects.filter(
                department__organization__tenant=self.request.tenant
            )
        
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not self.request.tenant:
            return Response({"error": "Tenant not found."}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()

    
        try:
            dept = Department.objects.get(
                name=data.get('department'),
                organization__tenant=self.request.tenant
            )
        except Department.DoesNotExist:
            return Response(
                {"error": "Department does not belong to your tenant or does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if not self.request.tenant:
            return Response({"error": "Tenant not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        customer = get_object_or_404(
            Customer,
            id=id,
        )
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
