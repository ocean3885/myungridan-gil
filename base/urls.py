from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('jmsubmit/', views.jmsubmit, name="jmsubmit"),
    path('msr/', views.msrInputView.as_view(), name="msr-input"),
    path('msr/<int:msr_id>', views.msrDetailView.as_view(), name="msr-detail"),
]