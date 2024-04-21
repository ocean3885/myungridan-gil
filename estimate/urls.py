from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.estimate_form, name="estimate-form"),
]