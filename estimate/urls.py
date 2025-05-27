from django.urls import path
from . import views

urlpatterns = [
    path('', views.estimate_form, name="estimate-form"),
    path('ajax/hanja/', views.get_hanja, name='get-hanja'),
    path('list/', views.estimate_list, name="estimate-list"),
    path('detail/<int:pk>/password', views.estimate_password, name="estimate-password"),
    path('detail/<int:pk>/', views.estimate_detail, name="estimate-detail"),
    path('detail/edit/<int:pk>/', views.estimate_form, name="estimate-edit"),
    path('detail/delete/<int:pk>/', views.estimate_delete, name="estimate-delete"),
    path('detail/<int:pk>/comment/', views.add_comment, name="add-comment"),
    path('detail/<int:post_id>/<int:comment_id>/', views.delete_comment, name="delete-comment"),

]