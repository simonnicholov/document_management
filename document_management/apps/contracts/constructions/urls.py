from django.urls import path
from . import views

app_name = 'constructions'

urlpatterns = [
    path('', views.index, name="index"),
    path('add/', views.add, name="add"),
    path('<int:id>/edit/', views.edit, name="edit"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:id>/details/', views.details, name="details"),
    path('<int:id>/upload/', views.upload, name="upload"),
]
