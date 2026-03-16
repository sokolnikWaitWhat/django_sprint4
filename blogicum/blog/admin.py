from django.contrib import admin
from .models import Category, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    list_filter = search_fields = list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at'
    )
    list_editable = (
        'is_published',
        'description',
        'slug'
    )
    list_display_links = ('title',)


class LocationAdmin(admin.ModelAdmin):
    list_filter = search_fields = list_display = (
        'name',
        'is_published',
        'created_at'
    )
    list_editable = ('is_published',)
    list_display_links = ('name',)


class PostAdmin(admin.ModelAdmin):
    list_filter = search_fields = list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at'
    )
    list_editable = (
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published'
    )
    list_display_links = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
