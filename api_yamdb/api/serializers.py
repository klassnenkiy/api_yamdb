import datetime

from rest_framework import serializers
from reviews.models import Categories, Genres, Titles


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Categories.objects.all()
    )

    class Meta:
        model = Titles
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )
        read_only_fields = ("id", "rating")

    def validate(self, data):
        if data["year"] > datetime.date.today().year:
            raise serializers.ValidationError(
                "Нельзя добавлять произведения, которые еще не вышли"
            )
        return data


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Genres


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "slug")
        model = Categories
