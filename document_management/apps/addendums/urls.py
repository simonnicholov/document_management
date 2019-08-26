from django.urls import path
from . import views

app_name = 'addendums'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:id>/lists/', views.lists, name="lists"),
    path('<int:id>/details/', views.details, name="details"),
    path('<int:id>/add/', views.add, name="add"),
    path('<int:id>/edit/', views.edit, name="edit"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:id>/upload/', views.upload, name="upload"),
    path('<int:id>/preview/', views.preview, name="preview"),
    path('<int:id>/status/', views.change_record_status, name="change_record_status"),
]
