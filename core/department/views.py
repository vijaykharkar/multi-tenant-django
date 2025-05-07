from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Department
from .serializers import DepartmentSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from organization.models import Organization


class DepartmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not self.request.tenant:
            return Response({"error": "Tenant not found."}, status=status.HTTP_400_BAD_REQUEST)
        organization_id = request.query_params.get('organization')

        departments = Department.objects.filter(
            organization__id=organization_id,
            organization__tenant=self.request.tenant
        )
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not self.request.tenant:
            return Response({"error": "Tenant not found."}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()

        try:
            org = Organization.objects.get(id=data.get('organization'))
        except Organization.DoesNotExist:
            return Response(
                {"error": "Organization does not belong to your tenant or does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DepartmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
       
        if not self.request.tenant:
            return Response({"error": "Tenant not found."}, status=status.HTTP_400_BAD_REQUEST)
        department = get_object_or_404(
            Department,
            id=id,
            organization__tenant=self.request.tenant
        )
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)
