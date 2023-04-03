import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title, User


class SignupSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=150
    )
    email = serializers.EmailField(required=True, max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username me запрещен'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=150
    )

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже есть!')
        return value

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
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


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class CommentSerializer(serializers.ModelSerializer):
    """Класс сериализатора Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Внутренний класс Meta."""
        fields = '__all__'
        model = Comment
        read_only_fields = ('title',)


class ReviewSerializer(serializers.ModelSerializer):
    """Класс сериализатора Review."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        """Внутренний класс Meta."""
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)
