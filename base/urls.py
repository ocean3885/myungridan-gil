from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    # path('profile/<int:pk>/', views.view_profile, name="view-profile"),
    # path('profile/<int:pk>/', views.view_profile, name="view-profile"),
]