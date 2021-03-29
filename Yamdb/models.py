from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from pytils.translit import slugify
from users.models import CustomUser

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

    class Meta:
        ordering = ['name', ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(
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

    class Meta:
        ordering = ['name', ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=200,
        blank=False,
        help_text='Напишите название произведения',
    )
    year = models.IntegerField()
    description = models.TextField(help_text='описание', null=True)
    genre = models.ManyToManyField(
        Genres,
        blank=True,
        related_name='genre_title',
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='category_title',
        db_index=False,
    )
    
    class Meta:
        ordering = ['id', ]

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    #user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    author = models.ForeignKey(
        CustomUser, blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='rev'
    )
    score = models.IntegerField(
        default=5,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    def __str__(self):
        return self.review_id
