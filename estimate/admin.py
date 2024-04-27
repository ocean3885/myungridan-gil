from django.contrib import admin
from .models import Estimate, Comment

class CommentInline(admin.StackedInline):
    model = Comment


class EstimateAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone','created', 'gen')
    inlines = (
        CommentInline,
    )

admin.site.register(Estimate, EstimateAdmin)

