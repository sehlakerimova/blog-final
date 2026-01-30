
from django.contrib import admin
from .models import Author, Category, Post, About,Comment, Tag, Like, Favorite, Report

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', 'categories')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(About)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Favorite)
admin.site.register(Report)
admin.site.register(Post)
