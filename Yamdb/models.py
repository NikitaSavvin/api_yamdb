from django.contrib.auth import get_user_model
from django.db import models
from pytils.translit import slugify

User = get_user_model()


class Categories(models.Model):
    name = models.CharField(
        'Категории',
        max_length=200,
        blank=False,
        null=False,
    )
    slug = models.SlugField(
        'Адрес страници категории',
        max_length=200,
        unique=True,
        help_text=(
            'Укажите адрес для страницы группы. Используйте только'
            'латиницу, цифры, дефисы и знаки подчёркивания'),
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)[:100]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class Genres(models.Model):
    genre = models.CharField(
        max_length=200,
        help_text='Напишите название жанра'
    )
    slug = models.SlugField(
        'Адрес страници жанра',
        max_length=200,
        unique=True,
        help_text=('Укажите адрес для страницы группы. Используйте только'
                   'латиницу, цифры, дефисы и знаки подчёркивания'),
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genre)[:100]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.genre


class Titles(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Название произведения',
        primary_key=True,
        blank=False,
        null=False,
    )
    year = models.IntegerField()
    description = models.TextField(help_text='описание')
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='genre_name',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='category_name',
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
