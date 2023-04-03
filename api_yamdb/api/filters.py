import django_filters
from reviews.models import Category, Genre, Title


class TitleFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(
        field_name='category__slug',
        to_field_name='category',
        queryset=Category.objects.all()
    )
    genre = django_filters.ModelChoiceFilter(
        field_name='genre__slug',
        to_field_name='genre',
        queryset=Genre.objects.all()
    )
    name = django_filters.ModelChoiceFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    year = django_filters.ModelChoiceFilter(
        field_name='year',
        lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = '__all__'