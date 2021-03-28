# Generated by Django 3.0.5 on 2021-03-26 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20210325_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bio',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('moderator', 'Moderator')], default='user', max_length=20, unique=True, verbose_name='User_status'),
        ),
    ]