from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление класса review"""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Набор объектов из базы данных."""
        title = get_object_or_404(Title, pk=self.kwargs.get('review_id'))
        return title.reviews

    def perform_create(self, serializer):
        """Сохранение нового отзыва."""
        title = get_object_or_404(Title, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление класса comment"""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Набор объектов из базы данных."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.comments

    def perform_create(self, serializer):
        """Сохранение нового комментария."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
