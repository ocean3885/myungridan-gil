from django.urls import path
from . import views

urlpatterns = [
    path('saju/', views.saju_list, name="saju-list"),
    path('create/', views.post_create, name="post-create"),
    path('lists/', views.post_list, name="post-list"),
    path('detail/<int:post_id>/', views.post_detail, name="post-detail"),
    path('detail/<int:post_id>/delete/', views.post_delete, name='post-delete'),
    path('detail/<int:post_id>/edit/', views.post_edit, name='post-edit'),
    path('detail/<int:post_id>/always/', views.post_always, name='post-always'),
    path('detail/<int:post_id>/sideview/', views.post_sideview, name='post-sideview'),
    path('naming/', views.naming_list, name="naming-list"),
    path('drafts/<int:draft_id>/publish/', views.publish_draft, name='publish_draft'),
]