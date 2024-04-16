from django.urls import path
from . import views

urlpatterns = [
    path('jm/', views.jm_submit, name="jm-submit"),
    path('gm/', views.gm_submit, name="gm-submit"),
    path('sj/', views.sj_submit, name="sj-submit"),
    path('etc/', views.etc_submit, name="etc-submit"),
    path('detail/<int:pk>/', views.submit_detail, name="submit-detail"),
]