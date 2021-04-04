from django.db.models import Avg, Max
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from users.utils import generate_confirmation_code, send_mail_to_user

from .filter import TitleFilter
from .mixins import ListCreateDestroyMixin
from .models import Categories, Genres, Review, Titles
from .permissions import (IsAdminOrReadOnly, IsAdminOrSuperUser,
                          IsAuthorOrStaffOrReadOnly)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          TitlesWriteSerializer, TitlesReadSerializer,
                          UserSerializer)

BASE_USERNAME = 'CustomUser'


class CategoriesViewSet(ListCreateDestroyMixin):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyMixin):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all().annotate(rating=Avg('reviews__score'))

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return TitlesReadSerializer
        else:
            return TitlesWriteSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class ReviewViewSet(viewsets.ModelViewSet):
    qureyset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrStaffOrReadOnly,
    ]

    def perform_create(self, serializer):
        data = {
            'author': self.request.user,
            'title': get_object_or_404(Titles, pk=self.kwargs.get('title_id')),
        }
        return serializer.save(**data)

    def get_queryset(self):
        title = get_object_or_404(
            Titles,
            pk=self.kwargs.get('title_id',)
        )
        all_review = title.reviews.all()
        return all_review


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorOrStaffOrReadOnly,
    ]

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
    permission_classes = [IsAdminOrSuperUser]
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


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email)
        if len(user) > 0:
            confirmation_code = user[0].confirmation_code
        else:
            confirmation_code = generate_confirmation_code()
            max_id = CustomUser.objects.aggregate(Max('id'))['id__max'] + 1
            data = {'email': email, 'confirmation_code': confirmation_code,
                    'username': f'{BASE_USERNAME}{max_id}'}
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        send_mail_to_user(email, confirmation_code)
        return Response({'email': email, })


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        user = get_object_or_404(CustomUser, email=request.data.get('email'))
        if user.confirmation_code != request.data.get('confirmation_code'):
            response = {'confirmation_code': 'Неверный код для данного email'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {'token': self.get_token(user)}
        return Response(response, status=status.HTTP_200_OK)
