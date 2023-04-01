import django_filters
from reviews.models import Category, Genre, Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(field_name='category__slug',
                                            to_field_name='category',
                                            queryset=Category.objects.all())
    genre = django_filters.ModelChoiceFilter(field_name='genre__slug',
                                            to_field_name='genre',
                                            queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = ('category', 'genre')