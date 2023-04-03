from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_token,
                    signup)

v1_router = DefaultRouter()
v1_router.register(
    'users',
    UserViewSet
)
v1_router.register(
    'categories',
    CategoryViewSet
)
v1_router.register(
    'genres',
    GenreViewSet
)
v1_router.register(
    'titles',
    TitleViewSet
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/auth/', include(auth_urlpatterns)),
    path('v1/', include(v1_router.urls)),
]
