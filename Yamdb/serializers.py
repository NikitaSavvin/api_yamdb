from rest_framework import serializers
from .models import Categories, Genres, Titles


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
