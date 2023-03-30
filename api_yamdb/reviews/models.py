from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Review(models.Model):
    """Модель, отвечает за отзывы в произведениях."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(settings.SCORE_ZERO),
            MaxValueValidator(settings.SCORE_TEN),
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        """Внутренний класс Meta."""
        default_related_name = 'reviews'


class Comment(models.Model):
    """Модель, отвечает за комментарии к отзывам."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Текст отзыва'
    )
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        """Внутренний класс Meta."""
        default_related_name = 'comments'
