from django.contrib import admin
from .models import Post, Text, Image

class TextInline(admin.TabularInline):  # 또는 admin.StackedInline
    model = Text
    extra = 1  # 기본적으로 보여질 폼의 수

class ImageInline(admin.TabularInline):  # 또는 admin.StackedInline
    model = Image
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [TextInline, ImageInline]

admin.site.register(Post, PostAdmin)
