# from django.utils.deprecation import MiddlewareMixin
# from django.utils import timezone
# from .models import PageView, PageViewDetail

# class PageViewMiddleware(MiddlewareMixin):
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         if request.path:
#             today = timezone.now().date()
#             page_view, created = PageView.objects.get_or_create(url=request.path)
#             page_view.total_views += 1
#             page_view.save()

#             page_view_detail, created = PageViewDetail.objects.get_or_create(page_view=page_view, date=today)
#             page_view_detail.views += 1
#             page_view_detail.save()
#         return None