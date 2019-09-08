from django.urls import path
from . import views

app_name = 'official_records'

urlpatterns = [
    path('', views.index, name="index"),

    path('related/', views.related, name="related"),
    path('unrelated/', views.unrelated, name="unrelated"),

    path('<int:id>/unrelated/preview/', views.unrelated_preview, name="unrelated_preview"),
    # path('<int:id>related//preview/', views.related_preview, name="related_preview"),

    path('unrelated/add/', views.unrelated_add, name="unrelated_add"),
    path('<int:id>/related/add/', views.related_add, name="related_add"),

    path('<int:id>/unrelated/edit/', views.unrelated_edit, name="unrelated_edit"),
    path('<int:id>/related/edit/', views.related_edit, name="related_edit"),

    path('<int:id>/unrelated/delete/', views.unrelated_delete, name="unrelated_delete"),
    path('<int:id>/related/delete/', views.related_delete, name="related_delete"),

    path('<int:id>/unrelated/details/', views.unrelated_details, name="unrelated_details"),
    path('<int:id>/related/details/', views.related_details, name="related_details"),

    path('<int:id>/unrelated/upload/', views.unrelated_upload, name="unrelated_upload"),
    path('<int:id>/related/upload/', views.related_upload, name="related_upload"),

    path('<int:id>/unrelated/change-record-status/', views.unrelated_change_record_status,
         name="unrelated_change_record_status"),
    path('<int:id>/related/change-record-status/', views.related_change_record_status,
         name="related_change_record_status"),

    path('<int:id>/related/lists/', views.related_lists, name="related_lists"),
    path('<int:id>/unrelated/change-status/', views.unrelated_change_status,
         name="unrelated_change_status"),
]
