from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenRefreshView)

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    RegisterView, ReviewViewSet, TitlesViewSet, TokenView,
                    UserViewSet)

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename='users')
v1_router.register('review', ReviewViewSet, basename='review')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment'
)
v1_router.register('categories', CategoriesViewSet, basename='v1_categories')
v1_router.register('genres', GenresViewSet, basename='v1_genres')
v1_router.register('titles', TitlesViewSet, basename='v1_titles')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/email/', RegisterView.as_view(),
         name='get_confirmation_code'),
    path('v1/auth/token/', TokenView.as_view(), name='get_token'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
