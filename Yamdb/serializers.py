from rest_framework import serializers
from .models import Categories, Genres, Titles
from django.db.models import Avg
from rest_framework.validators import UniqueTogetherValidator

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


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='id'
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Review
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_object_user',
            ),
            models.CheckConstraint(
                name='unique_object_author',
                check=~models.Q(user=models.F('author')),
            ),
        ]


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