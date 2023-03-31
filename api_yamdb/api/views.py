from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Categories, Genres, Titles


from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
)
from .filters import TitlesFilter


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.select_related("category")
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = TitlesFilter
    #filterset_fields = ("category__slug", "genre__slug", "name", "year")


class CreateListDeleteViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    pass


class CategoriesViewSet(CreateListDeleteViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenresViewSet(CreateListDeleteViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
