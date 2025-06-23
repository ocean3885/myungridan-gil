from django.contrib import admin
from .models import Post, Category, DraftPost
from django.urls import reverse
from django.utils.html import format_html

admin.site.register(Category)
admin.site.register(Post)

@admin.register(DraftPost)
class DraftPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at', 'publish_button')
    list_filter = ('user', 'category', 'created_at')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'

    # This method adds the "Publish" button to each row in the changelist
    def publish_button(self, obj):
        # Generate the URL for the publish action
        publish_url = reverse('publish_draft', args=[obj.pk])
        # Create an HTML link button
        return format_html('<a class="button" href="{}">Publish</a>', publish_url)
    
    publish_button.short_description = 'Actions' # Column header in admin
    publish_button.allow_tags = True # Required for rendering HTML

    




