from django.urls import path
from . import views

app_name = 'configurations'

urlpatterns = [
    path('category/', views.category, name="category"),
    path('<int:id>/list/', views.list, name="list"),
    path('<int:id>/add/', views.add, name="add"),
    path('<int:id>/edit/', views.edit, name="edit"),
    path('<int:id>/delete/', views.delete, name="delete"),
]
