from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from post.utils import CustomImageUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('post/', include('post.urls')),
    path('submit/', include('submit.urls')),
    path('estimate/', include('estimate.urls')),
    path('', include('base.urls')),    
    path('ckeditor/upload/', CustomImageUploadView.as_view(), name='ckeditor_upload'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)