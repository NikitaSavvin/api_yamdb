# Generated by Django 3.0.5 on 2021-03-23 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[('U', 'user'), ('M', 'moderator'), ('A', 'admin')], default=1, verbose_name='User_status'),
            preserve_default=False,
        ),
    ]
