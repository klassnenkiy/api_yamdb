from django.db import models

from .constants import (
    MAX_LENGTH_NAME_CATEGORY,
    MAX_LENGTH_NAME_GENRE,
    MAX_LENGTH_NAME_TITLE,
    MAX_LENGTH_SLUG_CATEGORY,
    MAX_LENGTH_SLUG_GENRE,
)


class Categories(models.Model):
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


class Genres(models.Model):
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


class Titles(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME_TITLE,
        verbose_name="Название произведения",
    )
    year = models.IntegerField(
        blank=True, null=True, verbose_name="Год выпуска"
    )
    rating = 1  # дописать ForeignKey после создания модели Рейтинга
    description = models.TextField(verbose_name="Описание произведения")
    genre = models.ManyToManyField(
        Genres,
        through="TitleGenre",
        blank=True,
        verbose_name="Жанр",
        help_text="Жанр произведения",
    )
    category = models.ForeignKey(
        Categories,
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


class TitleGenre(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.genre}"
