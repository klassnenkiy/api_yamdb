import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title, User


class SignupSerializer(serializers.Serializer):
    """Регистрация юзера"""
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
        """username не me"""
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username me запрещен'
            )
        return value


class TokenSerializer(serializers.Serializer):
    """Получение токена"""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Модель пользователя"""
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
    slug = serializers.SlugField(
        max_length=50,
    )

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Такой slug уже есть!')
        return value
    class Meta:
        model = Category
        fields = (
            "name",
            "slug"
        )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "name",
            "slug"
        )
        lookup_field = 'slug'

class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title

class TitleCreateSerializer(serializers.ModelSerializer):    
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field="slug",
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )
        model = Title

    def validate(self, data):
        if data["year"] <= 0 or data["year"] > datetime.date.today().year:
            raise serializers.ValidationError(
                "Нельзя добавлять произведения, которые еще не вышли"
            )
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            "name",
            "slug"
        )


class CommentSerializer(serializers.ModelSerializer):
    """Класс сериализатора Comment."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
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