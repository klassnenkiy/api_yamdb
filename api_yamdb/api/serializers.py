import datetime as dt

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class SignupSerializer(serializers.Serializer):
    '''Регистрация юзера'''
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
        '''username не me'''
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Username me запрещен'
            )
        return value


class TokenSerializer(serializers.Serializer):
    '''Получение токена'''
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    '''Модель пользователя'''
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
            'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(
        max_length=50,
        min_length=None,
        allow_blank=False
    )

    def validate_slug(self, value):
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError(
                'Такой slug уже есть!')
        return value

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = '__all__'

        def validate(self, data):
            if data['year'] > dt.date.today().year:
                raise serializers.ValidationError(
                    'Нельзя добавлять произведения, которые еще не вышли'
                )
            return data


class CommentSerializer(serializers.ModelSerializer):
    '''Класс сериализатора Comment.'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        '''Внутренний класс Meta.'''
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    '''Класс сериализатора Review.'''
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate_score(self, value):
        if 1 > value or value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть не менее 1 и не более 10'
            )
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(
            Title,
            pk=title_id
        )
        if request.method == 'POST' and Review.objects.filter(
            title=title,
            author=author
        ).exists():
            raise serializers.ValidationError(
                'Автор может поставить только одну оценку'
            )
        return data

    class Meta:
        '''Внутренний класс Meta.'''
        fields = '__all__'
        model = Review
