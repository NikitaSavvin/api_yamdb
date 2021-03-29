from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .filter import TitleFilter
from .models import Categories, Genres, Review, Titles, Titles
from .mixins import ListCreateDestroyMixin
from .permissions import IsAdminOrReadOnly, IsAdminOrSuperUser, IsAuthorOrModerator
from .serializers import (
    CategoriesSerializer,
    CommentSerializer,
    GenresSerializer,
    ReviewSerializer,
    TitlesSerializer,
    UserSerializer,
    TitleGetSerializer_NoRating
)
from users.models import CustomUser
from rest_framework.response import Response
from rest_framework import status


class CategoriesViewSet(ListCreateDestroyMixin):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyMixin):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().annotate(rating=Avg('reviews__score'))
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            serializer_class = TitlesSerializer # с полем rating
        else:
            serializer_class = TitleGetSerializer_NoRating
        return serializer_class 
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    #search_fields = ['category', ]
    #lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrModerator,]

    def perform_create(self, serializer):
        data = {
            'author': self.request.user,
            'title': get_object_or_404(Titles, pk=self.kwargs.get('title_id')),
        }
        serializer.save(**data)

    def get_queryset(self):
        title = get_object_or_404(
            Titles,
            pk=self.kwargs.get('title_id',)
        )
        all_review = title.reviews.all()
        return all_review


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrModerator,]

    def perform_create(self, serializer):
        data = {
            'author': self.request.user,
            'review': get_object_or_404(
                Review, pk=self.kwargs.get('review_id')
            ),
        }
        serializer.save(**data)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        all_comments = review.comments.all()
        return all_comments


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperUser,]
    lookup_field = "username"

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, username=request.user.username)
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid() and user.username == request.user.username:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
