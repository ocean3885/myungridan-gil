from django.urls import path
from . import views

urlpatterns = [
    path('saju/', views.saju_list, name="saju-list"),
    path('create/', views.post_create, name="post-create"),
    path('detail/<int:post_id>/', views.post_detail, name="post-detail"),
    path('detail/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('detail/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('naming/', views.naming_list, name="naming-list"),
]