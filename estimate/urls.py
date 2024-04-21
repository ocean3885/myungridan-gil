from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.estimate_form, name="estimate-form"),
    path('list/', views.estimate_list, name="estimate-list"),
    path('detail/<int:pk>/', views.estimate_detail, name="estimate-detail"),
    path('detail/edit/<int:pk>/', views.estimate_edit, name="estimate-edit"),
    path('detail/delete/<int:pk>/', views.estimate_delete, name="estimate-delete"),
]