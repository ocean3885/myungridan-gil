from django.urls import path
from . import views

urlpatterns = [
    path('', views.msrInputView.as_view(), name="msr-input"),
    path('<int:msr_id>', views.msrDetailView.as_view(), name="msr-detail"),
    path('home/', views.home, name="home"),
]