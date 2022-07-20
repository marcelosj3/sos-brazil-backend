from uuid import uuid4

from django.db import models


# Create your models here.
class Ong(models.Model):
    ong_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, null=True, unique=True)
    description = models.CharField(max_length=255, null=True, unique=True)
    cnpj = models.CharField(max_length=14, null=True, unique=True)
    site_address = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, null=True)
    created_at = models.DateField(auto_now=True)

    id = None
