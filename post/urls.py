from django.urls import path
from . import views

urlpatterns = [
    path('saju/', views.saju_list, name="saju-list"),
    path('create/', views.post_create, name="post-create"),
    path('detail/<int:post_id>/', views.post_detail, name="post-detail"),
    path('naming/', views.naming_list, name="naming-list"),
]