from django.db.models import F, Avg
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
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Titles

    def get_rating(self, obj):
        return obj.reviews.aggregate(avgs=Avg(F('score'))).get('avgs', None)
