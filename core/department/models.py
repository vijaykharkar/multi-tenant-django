from django.db import models
from organization.models import Organization

class Department(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name} ({self.organization.name})"