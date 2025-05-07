from django.urls import path
from .views import TenantListCreateView, TenantDetailView

urlpatterns = [
    path('tenant/', TenantListCreateView.as_view(), name='tenant-list'),
    path('tenant/<int:id>/', TenantDetailView.as_view(), name='tenant-detail')
]
