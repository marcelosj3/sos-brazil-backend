from uuid import uuid4

from django.db import models


class Campaign(models.Model):
    campaign_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    collected = models.FloatField(default=0)
    goal = models.FloatField()
    goal_reached = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()

    # ong = models.ManyToOneRel()  #TODO ForeignKey

    id = None


class Donation(models.Model):
    donation_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        "users.User", related_name="donations", on_delete=models.CASCADE
    )
    campaign = models.ForeignKey(
        "campaigns.Campaign", related_name="donations", on_delete=models.CASCADE
    )
    value = models.FloatField()
