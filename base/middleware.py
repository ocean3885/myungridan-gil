from django.utils.deprecation import MiddlewareMixin
from .models import PageView

class PageViewMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.path:
            page_view, created = PageView.objects.get_or_create(url=request.path)
            page_view.views += 1
            page_view.save()
        return response