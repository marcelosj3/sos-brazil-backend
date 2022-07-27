# Generated by Django 4.0.6 on 2022-07-26 04:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("ongs", "0001_initial"),
        ("campaigns", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="donations",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="campaign",
            name="ong",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="campaigns",
                to="ongs.ong",
            ),
        ),
    ]
