from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import UserViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
