from django.urls import path
from . import views

urlpatterns = [
    path('jm/', views.jm_submit, name="jm-submit"),
    path('gm/', views.gm_submit, name="gm-submit"),
    path('sj/', views.sj_submit, name="sj-submit"),
    path('etc/', views.etc_submit, name="etc-submit"),
    path('verify/', views.submit_verify, name="submit-verify"),
    path('list/<status>/', views.submit_list, name="submit-list"),
    path('list/', views.submit_list, name="submit-list"),
    path('detail/<int:pk>/', views.submit_detail, name="submit-detail"),
    path('detail/edit/<int:pk>/', views.submit_edit, name="submit-edit"),
    path('detail/delete/<int:pk>/', views.submit_delete, name="submit-delete"),
]