from django.urls import path
from .views import DepartmentListCreateView, DepartmentDetailView

urlpatterns = [
    path('department/', DepartmentListCreateView.as_view(), name='department-list'),
    path('department/<int:id>/', DepartmentDetailView.as_view(), name='department-detail') 
]