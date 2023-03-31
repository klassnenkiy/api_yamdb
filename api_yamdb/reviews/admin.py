from django.contrib import admin

from .models import Categories, Genres


class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class GenresAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Genres, GenresAdmin)
