from rest_framework import serializers
from .models import Categories, Genres, Titles


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Categories
        lookup_field = 'slug'
