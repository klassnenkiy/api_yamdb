from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Categories, Genres, Titles

from django.shortcuts import get_object_or_404

from .serializers import (
    CategoriesSerializer,
    GenresSerializer,
    TitlesSerializer,
)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.select_related("category")
    serializer_class = TitlesSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category__slug", "genre__slug", "name", "year")


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    pass


class DeleteViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class CategoryDeleteViewSet(DeleteViewSet):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        return get_object_or_404(Categories, slug=self.kwargs.get("slug"))


class GenresViewSet(CreateListViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GenreDeleteViewSet(DeleteViewSet):
    serializer_class = GenresSerializer

    def get_queryset(self):
        return get_object_or_404(Genres, slug=self.kwargs.get("slug"))
