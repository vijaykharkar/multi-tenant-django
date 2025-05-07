from django.urls import path
from .views import OrganizationListCreateView, OrganizationDetailView

urlpatterns = [
    path('organization/', OrganizationListCreateView.as_view(), name='organization-list'),
    path('organization/<int:id>/', OrganizationDetailView.as_view(), name='organization-detail')  
]