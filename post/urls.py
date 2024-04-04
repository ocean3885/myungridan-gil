from django.urls import path
from . import views

urlpatterns = [
    path('saju/', views.saju_list, name="saju-list"),
    path('create/', views.post_create, name="post-create"),
    path('lists/', views.post_list, name="post-list"),
    path('detail/<int:post_id>/', views.post_detail, name="post-detail"),
    path('detail/<int:post_id>/delete/', views.post_delete, name='post-delete'),
    path('detail/<int:post_id>/edit/', views.post_edit, name='post-edit'),
    path('naming/', views.naming_list, name="naming-list"),
]