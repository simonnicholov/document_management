from django.urls import path
from . import views

app_name = 'approval_requests'

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:id>/approve/', views.approve, name="approve"),
    path('<int:id>/reject/', views.reject, name="reject"),
]
