from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Organization
from .serializers import OrganizationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class OrganizationListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not self.request.tenant:
            return Response({"error": "Tenant not found."}, status=status.HTTP_400_BAD_REQUEST)
        # organizations = Organization.objects.filter(tenant=request.data.get('tenant'))
        organizations = Organization.objects.filter(tenant=self.request.tenant)
        serializer = OrganizationSerializer(organizations, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not self.request.tenant:
            return Response({"error": "Tenant not found."}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()

        serializer = OrganizationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if not self.request.tenant:
            return Response({"error": "Tenant not found."}, status=status.HTTP_400_BAD_REQUEST)
        organization = get_object_or_404(Organization, id=id, tenant=self.request.tenant)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)
