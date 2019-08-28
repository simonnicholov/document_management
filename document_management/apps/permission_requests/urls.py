from django.urls import path
from . import views

app_name = 'permission_requests'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:id>/details/', views.details, name="details"),
    path('<int:id>/<int:group>/requests/', views.requests, name="requests"),
]
