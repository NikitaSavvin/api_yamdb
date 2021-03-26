from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from .models import Titles, Genres, Categories
from .mixins import ListCreateDestroyMixin
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategoriesSerializer, TitlesSerializer, GenresSerializer, )


class CategoriesViewSet(ListCreateDestroyMixin):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyMixin):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['genre']
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'name', 'year']
    lookup_field = 'slug'
