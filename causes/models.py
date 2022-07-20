from django.db import models
from uuid import uuid4


class CauseModel(models.Model):
    cause_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, unique=True)

    id = None