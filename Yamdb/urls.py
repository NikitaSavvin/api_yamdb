from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet

router = DefaultRouter()
router.register('categories', CategoriesViewSet, basename='v1_categories')
router.register('genres', GenresViewSet, basename='v1_genres')
router.register(r'^genres/(?P<slug>[A-Za-z0-9_]+)', GenresViewSet)
router.register('titles', TitlesViewSet, basename='v1_titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
