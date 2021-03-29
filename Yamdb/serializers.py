from rest_framework import serializers
from .models import Categories, Genres, Titles, Review, Comment
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator
from django.db import models

from users.models import CustomUser


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Categories
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', 'slug']
        model = Genres


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return GenresSerializer(value).data


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        return CategoriesSerializer(value).data


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = '__all__'
        model = Titles


class TitleGetSerializer_NoRating(serializers.ModelSerializer):
    genre = GenreField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = CategoryField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('id', 'author', 'pub_date')
        model = Review
    def validate(self, data):
        user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if Review.objects.filter(author=user, pk=title_id).exists():
            raise serializers.ValidationError('Вы уже оставили отзыв.')
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        read_only_fields = ('review',)
        fields = '__all__'
        model = Comment




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('first_name', 'last_name', 'username',  'email', 'bio', 'role', )
        model = CustomUser

        validators = [UniqueTogetherValidator(
            queryset=CustomUser.objects.all(),
            fields=['email',])]