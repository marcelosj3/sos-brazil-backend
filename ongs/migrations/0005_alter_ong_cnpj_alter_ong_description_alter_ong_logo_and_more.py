# Generated by Django 4.0.6 on 2022-07-25 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ongs', '0004_alter_ong_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ong',
            name='cnpj',
            field=models.CharField(default='123', max_length=18, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ong',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ong',
            name='logo',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='ong',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='ong',
            name='site_address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]