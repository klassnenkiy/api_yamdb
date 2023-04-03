from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .constants import (MAX_LENGTH_NAME_CATEGORY, MAX_LENGTH_NAME_GENRE,
                        MAX_LENGTH_NAME_TITLE, MAX_LENGTH_SLUG_CATEGORY,
                        MAX_LENGTH_SLUG_GENRE)
from .validators import validate_username, validate_year


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    USER_ROLES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )

    username = models.CharField(
        validators=(validate_username,),
        max_length=150,
        unique=True,
        null=True
    )
    email = models.EmailField(
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=USER_ROLES,
        default=USER,
        blank=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_superuser
            or self.is_staff
        )

    @property
    def is_moderator(self):
        return (
            self.role == self.MODERATOR
        )


class Category(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME_CATEGORY,
        verbose_name="Категория",
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_SLUG_CATEGORY,
        verbose_name="Slug категории",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME_GENRE,
        verbose_name="Жанр",
    )
    slug = models.SlugField(
        unique=True,
        max_length=MAX_LENGTH_SLUG_GENRE,
        verbose_name="Slug жанра",
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME_TITLE,
        verbose_name="Название произведения",
        db_index=True
    )
    year = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name="Год выпуска",
        validators=(validate_year,)
    )
    rating = models.IntegerField(
        verbose_name="Рейтинг произведения",
        null=True,
        #blank=True,
        default=None,
    )
    description = models.TextField(
        verbose_name="Описание произведения",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        blank=True,
        related_name='titles',
        verbose_name="Жанр",
        help_text="Жанр произведения",
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="titles",
        verbose_name="Категория",
        help_text="Категория произведения",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'{self.title_id} - {self.genre_id}'


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

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель, отвечает за комментарии к отзывам."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Текст отзыва'
    )
    text = models.CharField(
        verbose_name='Текст комментария',
        max_length=256,
        help_text='Введите текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
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
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
