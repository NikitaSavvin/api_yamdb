# Generated by Django 3.0.5 on 2021-04-07 18:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yamdb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MaxValueValidator(10, 'Больше 10 поставить нельзя'), django.core.validators.MinValueValidator(1, 'Меньше 1 поставить нельзя')]),
        ),
    ]