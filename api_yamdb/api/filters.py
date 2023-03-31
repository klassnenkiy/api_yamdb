import django_filters

from reviews.models import Categories, Genres, Titles


class TitlesFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(field_name='category__slug',
                                            to_field_name='category',
                                            queryset=Categories.objects.all())
    genre = django_filters.ModelChoiceFilter(field_name='genre__slug',
                                            to_field_name='genre',
                                            queryset=Genres.objects.all())

    class Meta:
        model = Titles
        fields = ('category', 'genre')
