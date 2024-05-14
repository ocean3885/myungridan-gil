from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('map/', views.dowon_map, name="dowon-map"),
    path('namebase/', views.name_base, name="name-base"),
    path('sajubase/', views.saju_base, name="saju-base"),
    path('dowonqna/', views.dowon_qna, name="dowon-qna"),
    path('submitinfo/', views.submit_info, name="submit-info"),
    path('customer/list/', views.customer_list, name="customer-list"),
    path('customer/write/', views.customer_write, name="customer-write"),
    path('customer/<int:pk>/delete/', views.customer_delete, name="customer-delete"),
    path('customer/<int:pk>/edit/', views.customer_edit, name="customer-edit"),
    path('customer/<int:pk>/comment/write', views.customer_comment_write, name="customer-comment-write"),
    path('customer/<int:pk>/comment/<int:c_pk>/delete', views.customer_comment_delete, name="customer-comment-delete"),
    path('profile/<str:username>/', views.view_profile, name="view-profile"),
    path('profile/edit/<str:username>/', views.edit_profile, name="edit-profile"),
]