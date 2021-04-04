# Generated by Django 3.0.5 on 2021-04-03 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20210403_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='confirmation_code',
            field=models.CharField(default='KRFAKMJ212', max_length=100, null=True, verbose_name='Код подтверждения'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('moderator', 'Moderator')], default='user', max_length=20),
        ),
    ]
