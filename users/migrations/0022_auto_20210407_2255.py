# Generated by Django 3.0.5 on 2021-04-07 19:55

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20210407_2202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='confirmation_code',
            field=models.CharField(default=uuid.UUID('5820527e-76dd-42c8-95c4-1d17db254740'), max_length=100, null=True, verbose_name='Код подтверждения'),
        ),
    ]
