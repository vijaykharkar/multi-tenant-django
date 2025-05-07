from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser , User
from django.db import models

class Tenant_User(models.Model):
    tenant_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255, unique=True)
    domain = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

