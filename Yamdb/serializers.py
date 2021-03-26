from rest_framework import serializers
from .models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Categories
        lookup_field = 'slug'


class GenresSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Genres


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categories.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Titles
