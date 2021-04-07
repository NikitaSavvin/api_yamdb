from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (
    AllowAny, IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import CustomUser
from users.utils import send_mail_to_user

from .filter import TitleFilter
from .mixins import ListCreateDestroyMixin
from .models import Categories, Genres, Review, Titles
from .permissions import (
    IsAdminOrReadOnly, IsAdminOrSuperUser, IsAuthorOrStaffOrReadOnly
)
from .serializers import (
    CategoriesSerializer, CommentSerializer,
    EmailSerializer, GenresSerializer, ReviewSerializer,
    TitlesReadSerializer, TitlesWriteSerializer,
    TokenSerializer, UserSerializer
)


class CategoriesViewSet(ListCreateDestroyMixin):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenresViewSet(ListCreateDestroyMixin):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
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
                Review,
                title__id=self.kwargs.get('title_id'),
                id=self.kwargs.get('review_id')
            ),
        }
        serializer.save(**data)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            title__id=self.kwargs.get('title_id'),
            id=self.kwargs.get('review_id')
        )
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
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def RegisterView(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = request.data.get('email')
    user, create = CustomUser.objects.get_or_create(
        email=serializer.validated_data.get('email'))
    if create:
        user.username = serializer.validated_data.get('email')
        user.save()
    token = default_token_generator.make_token(user)
    email_to = email
    message = f'Код подтверждения:{token}'
    send_mail_to_user(email_to, message,)
    return Response(
        f'Код подтверждения будет отправлен вам на почту: {user.email}'
    )


@api_view(['POST'],)
@permission_classes([AllowAny, ])
def GetTokenView(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(CustomUser, email=serializer.validated_data.get(
        'email'))
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response({'Токен': f'{token.access_token}'})
    return Response(status=status.HTTP_400_BAD_REQUEST)
