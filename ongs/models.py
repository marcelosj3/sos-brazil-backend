from uuid import uuid4

from django.db import models


# Create your models here.
class Ong(models.Model):
    ong_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    # TODO create a mask to force the user to use our pattern,
    # that is "X.XXX.XXX/0001-XX"
    cnpj = models.CharField(max_length=18, unique=True)
    site_address = models.CharField(max_length=255, null=True)
    logo = models.CharField(max_length=255)
    created_at = models.DateField(auto_now=True)

    causes = models.ManyToManyField("causes.Cause", related_name="ongs")
    admins = models.ManyToManyField("users.User", related_name="ongs")

    id = None
