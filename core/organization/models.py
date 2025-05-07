from django.db import models
from tenant.models import Tenant_User


class Organization(models.Model):
    tenant = models.ForeignKey(Tenant_User, on_delete=models.CASCADE, related_name='organizations')
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.name} ({self.tenant.name})"
