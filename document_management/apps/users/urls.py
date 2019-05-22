from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # External
    path('login/', views.login_view, name="login_view"),

    # Internal
    path('', views.index, name="index"),
    path('add/', views.add, name="add"),
    path('<int:id>/edit/', views.edit, name="edit"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:id>/details/', views.details, name="details"),
    path('<int:id>/reset-password/', views.reset_password, name="reset_password"),
]
