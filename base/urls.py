from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('map/', views.dowon_map, name="dowon-map"),
    path('profile/<str:username>/', views.view_profile, name="view-profile"),
    path('profile/edit/<str:username>/', views.edit_profile, name="edit-profile"),
]