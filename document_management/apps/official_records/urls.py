from django.urls import path
from . import views

app_name = 'official_records'

urlpatterns = [
    path('', views.index, name="index"),

    path('related/', views.related, name="related"),
    path('unrelated/', views.unrelated, name="unrelated"),

    path('unrelated/<int:id>/preview/', views.unrelated_preview, name="unrelated_preview"),
    path('related/<int:id>/preview/', views.related_preview, name="related_preview"),

    path('unrelated/add/', views.unrelated_add, name="unrelated_add"),
    path('related/<int:id>/add/', views.related_add, name="related_add"),

    path('unrelated/<int:id>/edit/', views.unrelated_edit, name="unrelated_edit"),
    path('related/<int:id>/edit/', views.related_edit, name="related_edit"),

    path('unrelated/<int:id>/delete/', views.unrelated_delete, name="unrelated_delete"),
    path('related/<int:id>/delete/', views.related_delete, name="related_delete"),

    path('unrelated/<int:id>/details/', views.unrelated_details, name="unrelated_details"),
    path('related/<int:id>/details/', views.related_details, name="related_details"),

    path('unrelated/<int:id>/upload/', views.unrelated_upload, name="unrelated_upload"),
    path('related/<int:id>/upload/', views.related_upload, name="related_upload"),

    path('unrelated/<int:id>/change-record-status/', views.unrelated_change_record_status,
         name="unrelated_change_record_status"),
    path('related/<int:id>/change-record-status/', views.related_change_record_status,
         name="related_change_record_status"),

    path('related/<int:id>/lists/', views.related_lists, name="related_lists"),
    path('unrelated/<int:id>/change-status/', views.unrelated_change_status,
         name="unrelated_change_status"),

    path('unrelated/<int:id>/remove/', views.unrelated_remove, name="unrelated_remove"),
]
