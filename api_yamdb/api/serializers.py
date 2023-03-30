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
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        exclude = ('id', )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'