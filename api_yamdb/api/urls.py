from rest_framework import routers

from django.urls import include, path

from api.views import (
    CategoriesViewSet,
    CategoryDeleteViewSet,
    GenreDeleteViewSet,
    GenresViewSet,
    TitlesViewSet,
)


router = routers.DefaultRouter()
router.register("titles", TitlesViewSet)
router.register("categories", CategoriesViewSet)
router.register("genres", GenresViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
