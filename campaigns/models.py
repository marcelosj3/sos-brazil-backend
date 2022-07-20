from uuid import uuid4

from django.db import models


class Campaign(models.Model):
    campaign_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    collected = models.FloatField()
    goal = models.FloatField(null=True)
    goal_reached = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()

    # ong = models.ManyToOneRel()  #TODO ForeignKey

    id = None
