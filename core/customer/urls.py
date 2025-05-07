from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView

urlpatterns = [
    path('customer/', CustomerListCreateView.as_view(), name='customer-list'),
    path('customer/<int:id>/', CustomerDetailView.as_view(), name='customer-detail') 
]