# Generated by Django 3.0.5 on 2021-03-26 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210326_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('moderator', 'Moderator')], default='user', max_length=20, verbose_name='User_status'),
        ),
    ]
