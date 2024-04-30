from django.urls import path
from . import views

urlpatterns = [
    path('form/<category>/', views.submit_form, name="submit-form"),
    path('verify/', views.submit_verify, name="submit-verify"),
    path('verify/list', views.submit_verify_list, name="submit-verify-list"),
    path('list/<status>/', views.submit_list, name="submit-list"),
    path('list/', views.submit_list, name="submit-list"),
    path('detail/<int:pk>/', views.submit_detail, name="submit-detail"),
    path('detail/edit/<int:pk>/', views.submit_edit, name="submit-edit"),
    path('detail/delete/<int:pk>/', views.submit_delete, name="submit-delete"),
    path('detail/payok/<int:pk>/', views.pay_ok, name="pay-ok"),
    path('detail/payno/<int:pk>/', views.pay_no, name="pay-no"),
    path('detail/complete/<int:pk>/', views.complete, name="complete"),
]