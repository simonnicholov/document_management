from django.urls import path
from . import views

app_name = 'contracts'

urlpatterns = [
    path('', views.index, name="index"),
    path('add/', views.add, name="add"),
    path('<int:id>/edit/', views.edit, name="edit"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:id>/details/', views.details, name="details"),
    path('<int:id>/upload/', views.upload, name="upload"),
    path('<int:id>/change-status/', views.change_status, name="change_status"),
    path('<int:id>/change-record-status/', views.change_record_status, name="change_record_status"),
    path('<int:id>/preview/', views.preview, name="preview"),
]
