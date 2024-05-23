from django.contrib import admin
from .models import Profile, CustomBoard, PageView, PageViewDetail


class PageViewAdmin(admin.ModelAdmin):
    list_display = ('url', 'total_views')
    search_fields = ('url',)

class PageViewDetailAdmin(admin.ModelAdmin):
    list_display = ('page_view', 'date', 'views')
    list_filter = ('date',)
    search_fields = ('page_view__url',)

admin.site.register(Profile)
admin.site.register(CustomBoard)
admin.site.register(PageView, PageViewAdmin)
admin.site.register(PageViewDetail, PageViewDetailAdmin)
