from rest_framework import serializers

from ..reviews.models import Comment, Review


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
