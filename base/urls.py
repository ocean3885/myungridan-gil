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
    path('profile/<str:username>/', views.view_profile, name="view-profile"),
    path('profile/edit/<str:username>/', views.edit_profile, name="edit-profile"),
]