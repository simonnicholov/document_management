from django.urls import path, include

from . import views

app_name = 'apps'

urlpatterns = [
    # namespace urls
    path('', include('document_management.apps.users.urls', namespace="users")),
    path('location/', include('document_management.apps.locations.urls', namespace="locations")),

    # specific urls
    path('dashboard/', views.dashboard, name="dashboard"),
]