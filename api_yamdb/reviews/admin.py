from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = (
        'name',
        'slug',
    )


class GenreResource(resources.ModelResource):
    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'slug',
        )


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    list_display = (
        'name',
        'slug',
    )


class TitleResource(resources.ModelResource):
    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
        )


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    list_display = (
        'name',
        'year',
        'category',
    )


class GenreTitleResource(resources.ModelResource):
    class Meta:
        model = GenreTitle
        fields = (
            'id',
            'title_id',
            'genre_id',
        )


@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = [GenreTitleResource]
    list_display = (
        'title_id',
        'genre_id',
    )


class ReviewsResource(resources.ModelResource):
    class Meta:
        model = Review
        fields = (
            'id',
            'title_id',
            'text',
            'author',
            'score',
            'pub_date',
        )


@admin.register(Review)
class ReviewsAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewsResource]
    list_display = (
        'text',
        'author',
        'score',
        'pub_date',
    )


class CommentsResource(resources.ModelResource):
    class Meta:
        model = Comment
        fields = (
            'id',
            'review_id',
            'text',
            'author',
            'pub_date',
        )


@admin.register(Comment)
class CommentsAdmin(ImportExportModelAdmin):
    resource_classes = [CommentsResource]
    list_display = (
        'text',
        'author',
        'pub_date',
    )
