# Generated by Django 3.0.5 on 2021-04-05 11:13

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_auto_20210403_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='confirmation_code',
            field=models.CharField(default=uuid.UUID('d52fe198-2464-49fd-ae93-af4b108cfe71'), max_length=100, null=True, verbose_name='Код подтверждения'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'admin'), ('user', 'user'), ('moderator', 'moderator')], default='user', max_length=20),
        ),
    ]
