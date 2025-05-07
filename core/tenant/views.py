from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Tenant_User
from .serializers import TenantSerializer, RegisterSerializer, LoginSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token




class TenantListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tenants = Tenant_User.objects.all()
        serializer = TenantSerializer(tenants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TenantSerializer(data=request.data)
        if serializer.is_valid():
            print("serializer*****************",serializer)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TenantDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id):
        tenant = get_object_or_404(Tenant_User, id=id)
        serializer = TenantSerializer(tenant)
        return Response(serializer.data)
    

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({'status':False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        user=serializer.save()
        
        return Response({'status':True,'message':'User created successfully','data': RegisterSerializer(user).data}, status=status.HTTP_201_CREATED)

       
class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({'status':False,'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)   
        
        user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
        if user is None:
            return Response({'status':False,'message':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)    
       
        token, _ = Token.objects.get_or_create(user=user)
      
        return Response({
            'status':True, 
            'message':'Login successful',
            'token':str(token)}, 
            status=status.HTTP_200_OK
            )
        
