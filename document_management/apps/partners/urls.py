from django.urls import path
from . import views

app_name = 'partners'

urlpatterns = [
    path('', views.index, name="index"),
    path('add/', views.add, name="add"),
    # for now, this is unavaiable at phase one
    path('search/', views.search, name="search"),
    path('<int:id>/edit/', views.edit, name="edit"),
    path('<int:id>/delete/', views.delete, name="delete"),
    path('<int:id>/details/', views.details, name="details"),
    path('<int:id>/change-record-status/', views.change_record_status, name="change_record_status"),
]
