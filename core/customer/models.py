from django.db import models
from department.models import Department


class Customer(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.name} ({self.department.name})"